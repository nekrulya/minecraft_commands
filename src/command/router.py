from datetime import datetime
from typing import Annotated

from databases import Database
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select, insert, update, delete
from starlette import status
import re
import yaml

from starlette.responses import FileResponse

from src.auth.exceptions import UserNotFound
from src.auth.models import User
from src.auth.token_util import verify_token
from src.auth.utils import get_user_by_username
from src.command.exceptions import CommandNotFoundError, CommandEmptyNameError, CommandEmptyDescriptionError, \
    CommandNameIsTakenError, CommandForbiddenActionError, CommandNameError
from src.command.models import Command
from src.command.schemas import CommandCreate, CommandUpdate, CommandCreateResponse, CommandReadResponse, \
    CommandUpdateResponse, CommandDeleteResponse
from src.command.utils import get_command_by_id, get_command_by_name
from src.database import get_db

router = APIRouter(
    prefix="/command",
    tags=["command"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

name_pattern = r'^[A-Za-zА-Яа-яЁё0-9_ ]+$'


@router.get("", summary="One or all commands")
async def get_command(
        command_id: int | None = None,
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1)] = 10,
        db: Database = Depends(get_db),
) -> CommandReadResponse | list[CommandReadResponse]:
    """
        **command_id**: if None -> list of all commands, else specific by id\n
        **offset**: from the beginning\n
        **limit**: how many commands to return
    """
    # Получение всех команд
    if command_id is None:
        query = select(
            Command,
            User.username.label('created_by')
        ).join(User).order_by(Command.name)
        commands = await db.fetch_all(query)
        return commands[offset:offset + limit]

    # Получение конкретной команды
    command = await get_command_by_id(command_id, username=True, db=db)
    if command is None:
        raise CommandNotFoundError()

    return command

@router.post("")
async def command_create(
        command: CommandCreate,
        token : str = Depends(oauth2_scheme),
        db: Database = Depends(get_db),
) -> CommandCreateResponse:
    name, description = command.name.strip().lower(), command.description.strip().lower()
    name = "_".join(name.split())
    description = "_".join(description.split())

    if name == '':
        raise CommandEmptyNameError()

    if description == '':
        raise CommandEmptyDescriptionError()

    if await get_command_by_name(name, db=db):
        raise CommandNameIsTakenError()

    if not re.fullmatch(name_pattern, name):
        raise CommandNameError()

    token = verify_token(token)
    username = token["username"]
    user = await get_user_by_username(username, db=db)

    # Проверка наличия пользователя
    if user is None:
        raise UserNotFound()

    try:
        query = insert(Command).values(
            name=name,
            description=description,
            created_by=user.id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        new_command_id = await db.execute(query)
        command = await get_command_by_id(new_command_id, db=db)
        return command

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Command creating error"
        )

@router.put("/{command_id}")
async def command_update(
        command_id: int,
        command_data: CommandUpdate,
        token : str = Depends(oauth2_scheme),
        db: Database = Depends(get_db),
) -> CommandUpdateResponse:

    name, description = command_data.name.strip().lower(), command_data.description.strip().lower()
    name = "_".join(name.split())
    description = "_".join(description.split())

    if name == '':
        raise CommandEmptyNameError()

    if description == '':
        raise CommandEmptyDescriptionError()

    if not re.fullmatch(name_pattern, name):
        raise CommandNameError()

    command = await get_command_by_id(command_id, db)

    # Проверка наличия команды
    if command is None:
        raise CommandNotFoundError()

    if await get_command_by_name(name, db=db) and name != command.name:
        raise CommandNameIsTakenError()

    token = verify_token(token)
    user = await get_user_by_username(token["username"], db=db) if token else None

    # Проверка наличия пользователя
    if user is None:
        raise UserNotFound()

    # Проверка принадлежности команды пользователю
    if user.id != command.created_by:
        raise CommandForbiddenActionError()

    update_data = {
        "name": name,
        "description": description,
        "updated_at": datetime.now(),
    }

    query = (
        update(Command)
        .where(Command.id == command_id)
        .values(update_data)
        .returning(Command)
    )
    await db.execute(query)

    command = await get_command_by_id(command_id, db)
    return command

@router.delete("/{command_id}")
async def command_delete(
        command_id: int,
        token : str = Depends(oauth2_scheme),
        db: Database = Depends(get_db),
) -> CommandDeleteResponse:
    # Проверка наличия записи
    command = await get_command_by_id(command_id, db=db)
    if command is None:
        raise CommandNotFoundError()

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    token = verify_token(token)
    user = await get_user_by_username(token["username"], db=db) if token else None

    # Проверка наличия пользователя
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username"
        )

    # Проверка принадлежности команды пользователю
    if user.id != command.created_by:
        raise CommandForbiddenActionError()

    query = delete(Command).where(Command.id == command_id)
    await db.execute(query)

    return CommandDeleteResponse(name=command.name, description=command.description)

@router.get('/file')
async def get_file(db: Database = Depends(get_db)) -> FileResponse:
    query = select(Command).order_by(Command.name)
    commands = await db.fetch_all(query)
    commands_to_yaml = {
        "command-block-overrides": [],
        "ignore-vanilla-permissions": False,
        "aliases": {
            "icanhasbukkit": ["version $1-"],
        }
    }
    commands_data = {command.name: [command.description.strip("/")] for command in commands}
    commands_to_yaml["aliases"].update(commands_data)

    with open("commands.yaml", mode="w", encoding="utf-8") as f:
        yaml.dump(commands_to_yaml, stream=f, default_flow_style=False, indent=4, sort_keys=False, allow_unicode=True)

    return FileResponse("commands.yaml", status_code=status.HTTP_200_OK)