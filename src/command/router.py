from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select, insert, update, delete
from starlette import status

from src.auth.exceptions import UserNotFound
from src.auth.models import User
from src.auth.token_util import verify_token
from src.auth.utils import get_user_by_username
from src.command.exceptions import CommandNotFoundError, CommandEmptyNameError, CommandEmptyDescriptionError, \
    CommandNameIsTakenError, CommandForbiddenActionError
from src.command.models import Command
from src.command.schemas import CommandCreate, CommandUpdate, CommandCreateResponse, CommandReadResponse, \
    CommandUpdateResponse, CommandDeleteResponse
from src.command.utils import get_command_by_id, get_command_by_name
from src.database import database

router = APIRouter(
    prefix="/command",
    tags=["command"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


@router.get("")
async def get_command(
        command_id: int | None = None,
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1)] = 10
) -> CommandReadResponse | list[CommandReadResponse]:
    # Получение всех команд
    if command_id is None:
        query = select(
            Command,
            User.username.label('created_by')
        ).join(User).order_by(Command.name)
        commands = await database.fetch_all(query)
        return commands[offset:offset + limit]

    # Получение конкретной команды
    command = await get_command_by_id(command_id, username=True)
    if command is None:
        raise CommandNotFoundError()

    return command

@router.post("")
async def command_create(
        command: CommandCreate,
        token : str = Depends(oauth2_scheme)
) -> CommandCreateResponse:

    if command.name.strip() == '':
        raise CommandEmptyNameError()

    if command.description.strip() == '':
        raise CommandEmptyDescriptionError()

    if await get_command_by_name(command.name):
        raise CommandNameIsTakenError()

    token = verify_token(token)
    username = token["username"]
    user = await get_user_by_username(username)

    # Проверка наличия пользователя
    if user is None:
        raise UserNotFound()

    try:
        stmt = insert(Command).values(
            name=command.name.lower().strip(),
            description=command.description.lower().strip(),
            created_by=user.id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        new_command_id = await database.execute(stmt)
        command = await get_command_by_id(new_command_id)
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
        token : str = Depends(oauth2_scheme)
) -> CommandUpdateResponse:

    if command_data.name.strip() == '':
        raise CommandEmptyNameError()

    if command_data.description.strip() == '':
        raise CommandEmptyDescriptionError()

    command = await get_command_by_id(command_id)

    # Проверка наличия команды
    if command is None:
        raise CommandNotFoundError()

    if await get_command_by_name(command_data.name) and command_data.name != command.name:
        raise CommandNameIsTakenError()

    token = verify_token(token)
    user = await get_user_by_username(token["username"]) if token else None

    # Проверка наличия пользователя
    if user is None:
        raise UserNotFound()

    # Проверка принадлежности команды пользователю
    if user.id != command.created_by:
        raise CommandForbiddenActionError()

    update_data = command_data.model_dump()
    update_data["name"] = update_data["name"].lower().strip()
    update_data["description"] = update_data["description"].lower().strip()
    update_data["updated_at"] = datetime.now()

    query = (
        update(Command)
        .where(Command.id == command_id)
        .values(update_data)
        .returning(Command)
    )
    await database.execute(query)

    command = await get_command_by_id(command_id)
    return command

@router.delete("/{command_id}")
async def command_delete(
        command_id: int,
        token : str = Depends(oauth2_scheme)
) -> CommandDeleteResponse:
    # Проверка наличия записи
    command = await get_command_by_id(command_id)
    if command is None:
        raise CommandNotFoundError()

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    token = verify_token(token)
    user = await get_user_by_username(token["username"]) if token else None

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
    await database.execute(query)

    return CommandDeleteResponse(name=command.name, description=command.description)