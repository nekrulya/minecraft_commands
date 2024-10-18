from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select, insert, update
from starlette import status
from starlette.responses import JSONResponse

from src.auth.models import User
from src.auth.token_util import verify_token
from src.auth.utils import get_user_by_username
from src.command.models import Command
from src.command.schemas import CommandCreate, CommandUpdate
from src.database import database

router = APIRouter(
    prefix="/command",
    tags=["command"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

@router.get("/all")
async def get_all_commands():
    query = select(Command).order_by(Command.name)
    commands = await database.fetch_all(query)
    return commands

@router.get("/{command_id}")
async def get_command_by_id(command_id: int):
    query = select(Command).where(Command.id == command_id)
    command = await database.fetch_one(query)

    # Проверка наличия команды
    if command is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Command not found")

    return command

@router.post("/create")
async def command_create(
        command: CommandCreate,
        token : str = Depends(oauth2_scheme)):

    token = verify_token(token)
    username = token["username"]
    user = await get_user_by_username(username)

    # Проверка наличия пользователя
    if user is None:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username"
        )

    try:
        stmt = insert(Command).values(
            name=command.name,
            description=command.description,
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
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Command creating error"
        )

@router.put("/update")
async def command_update(
        command_id: int,
        command_data: CommandUpdate,
        token : str = Depends(oauth2_scheme)):

    query = select(Command).where(Command.id == command_id)
    command = await database.fetch_one(query)

    # Проверка наличия команды
    if command is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Command not found"
        )

    token = verify_token(token)
    user = await get_user_by_username(token["username"])

    # Проверка наличия пользователя
    if user is None:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username"
        )

    # Проверка принадлежности команды пользователю
    if user.id != command.id:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )

    update_data = command_data.model_dump()
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

