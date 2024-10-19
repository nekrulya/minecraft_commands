from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select, insert, update, delete
from starlette import status
from starlette.responses import JSONResponse

from src.auth.models import User
from src.auth.token_util import verify_token
from src.auth.utils import get_user_by_username
from src.command.models import Command
from src.command.schemas import CommandCreate, CommandUpdate
from src.command.utils import get_command_by_id, get_command_by_name
from src.database import database

router = APIRouter(
    prefix="/command",
    tags=["command"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


@router.get("")
async def get_command(command_id: int | None = None):
    # Получение всех команд
    if command_id is None:
        query = select(
            Command.id,
            Command.name,
            Command.description,
            User.username.label('created_by')
        ).join(User).order_by(Command.name)
        commands = await database.fetch_all(query)
        return commands

    # Получение конкретной команды
    command = await get_command_by_id(command_id)
    return command

@router.post("")
async def command_create(
        command: CommandCreate,
        token : str = Depends(oauth2_scheme)):

    if command.name.strip() == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name cannot be empty")

    if command.description.strip() == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Description cannot be empty")

    token = verify_token(token)
    username = token["username"]
    user = await get_user_by_username(username)

    if await get_command_by_name(command.name):
        raise HTTPException(status_code=400, detail="Command name is taken")

    # Проверка наличия пользователя
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username"
        )

    try:
        stmt = insert(Command).values(
            name=command.name.lower().strip(),
            description=command.description.lower().strip(),
            created_by=user.id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        await database.execute(stmt)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content="Command created successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Command creating error"
        )

@router.put("/{command_id}")
async def command_update(
        command_id: int,
        command_data: CommandUpdate,
        token : str = Depends(oauth2_scheme)):

    if command_data.name.strip() == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name cannot be empty")

    if command_data.description.strip() == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Description cannot be empty")

    command = await get_command_by_id(command_id)

    if command is None:
        raise HTTPException(status_code=404, detail="Command not found")


    if await get_command_by_name(command_data.name) and command_data.name != command.name:
        raise HTTPException(status_code=400, detail="Command name is taken")

    token = verify_token(token)
    user = await get_user_by_username(token["username"])

    # Проверка наличия пользователя
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username"
        )

    # Проверка принадлежности команды пользователю
    if user.id != command.created_by:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )

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

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content="Command updated successfully"
    )

@router.delete("/{command_id}")
async def command_delete(
        command_id: int,
        token : str = Depends(oauth2_scheme)
        ):
    # Проверка наличия записи
    command = await get_command_by_id(command_id)

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    token = verify_token(token)
    user = await get_user_by_username(token["username"])

    # Проверка наличия пользователя
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username"
        )

    # Проверка принадлежности команды пользователю
    if user.id != command.created_by:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )

    query = delete(Command).where(Command.id == command_id)
    await database.execute(query)

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content="Command deleted successfully"
    )