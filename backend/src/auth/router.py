from databases import Database
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy import select
from starlette import status
from starlette.responses import JSONResponse

from backend.src.auth.exceptions import UserAlreadyExists, UserNotFound, UsernameIncorrectData
from backend.src.auth.models import User
from backend.src.auth.schemas import UserCreate, UserCreateResponse, UserReadResponse
from backend.src.auth.token_util import create_access_token
from backend.src.auth.utils import create_user, get_user_by_username, verify_password
from backend.src.command.schemas import CommandReadResponse
from backend.src.command.utils import get_commands_by_user_id
from backend.src.database import get_db

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

@router.get("/")
async def get_user(
        username: str | None = None,
        db: Database = Depends(get_db)
) -> UserReadResponse | list[UserReadResponse]:
    if username is None:
        query = select(User).order_by(User.username)
        users = await db.fetch_all(query)
        return [UserReadResponse(username=user.username, id=user.id) for user in users]

    user = await get_user_by_username(username, db=db)
    return UserReadResponse(username=user.username, id=user.id)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
        user: UserCreate,
        db: Database = Depends(get_db)
) -> UserCreateResponse:
    existing_user = await get_user_by_username(user.username, db=db)
    if existing_user:
        raise UserAlreadyExists()

    await create_user(user.username, user.password, db=db)
    user = await get_user_by_username(user.username, db=db)
    return UserCreateResponse(username=user.username)

@router.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Database = Depends(get_db)
) -> JSONResponse:
    user = await get_user_by_username(form_data.username, db=db)
    if not user:
        raise UserNotFound()
    if not verify_password(form_data.password, user.hashed_password):
        raise UsernameIncorrectData()

    access_token = create_access_token({"username": user.username})
    return JSONResponse(status_code=200, content={"access_token": access_token, "token_type": "bearer"})


@router.get("/commands")
async def get_user_commands(username: str, db: Database = Depends(get_db)) -> list[CommandReadResponse]:
    user = await get_user_by_username(username, db=db)
    if user is None:
        raise UserNotFound()
    commands = await get_commands_by_user_id(user_id=user.id, db=db)
    return commands[:]
