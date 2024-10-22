from databases import Database
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy import select
from starlette import status
from starlette.responses import JSONResponse

from src.auth.exceptions import UserAlreadyExists, UserNotFound, UsernameIncorrectData
from src.auth.models import User
from src.auth.schemas import UserCreate, UserCreateResponse
from src.auth.token_util import create_access_token
from src.auth.utils import create_user, get_user_by_username, verify_password, get_user_dict
from src.database import get_db

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

@router.get("/")
async def get_user(
        username: str | None = None,
        db: Database = Depends(get_db)
):
    if username is None:
        query = select(User).order_by(User.username)
        users = await db.fetch_all(query)
        response = []
        for user in users:
            response.append(get_user_dict(user))
        return response

    user = await get_user_by_username(username, db=db)
    return user

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
    return user

@router.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Database = Depends(get_db)
):
    user = await get_user_by_username(form_data.username, db=db)
    if not user:
        raise UserNotFound()
    if not verify_password(form_data.password, user.hashed_password):
        raise UsernameIncorrectData()

    access_token = create_access_token({"username": user.username})
    return JSONResponse(status_code=200, content={"access_token": access_token, "token_type": "bearer"})


@router.get("/user_commands")
async def get_user_commands(user_id: int, db: Database = Depends(get_db)):
    user = await db.fetch_one(select(User).where(User.id == user_id))
    return user