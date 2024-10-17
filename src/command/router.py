from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select, insert
from starlette import status
from starlette.responses import JSONResponse

from src.auth.models import User
from src.auth.token_util import verify_token
from src.auth.utils import get_user_by_username
from src.command.models import Command
from src.command.schemas import CommandCreate
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
    return JSONResponse(content=commands)

@router.post("/create")
async def command_create(command: CommandCreate, token : str = Depends(oauth2_scheme)):
    res = verify_token(token)
    username = res["username"]
    user = await get_user_by_username(username)
    if user is None:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username")

    try:
        stmt = insert(Command).values(name=command.name, description=command.description, created_by=username)
        await database.execute(stmt)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="Command created successfully")
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Command creating error")

