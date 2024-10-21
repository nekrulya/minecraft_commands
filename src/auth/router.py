from databases import Database
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy import select
from starlette.responses import JSONResponse

from src.auth.models import User
from src.auth.schemas import UserCreate
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

@router.post("/register")
async def register_user(
        user: UserCreate,
        db: Database = Depends(get_db)
):
    existing_user = await get_user_by_username(user.username, db=db)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    await create_user(user.username, user.password, db=db)
    return JSONResponse(
        status_code=201,
        content={"username": user.username}
    )

@router.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Database = Depends(get_db)
):
    user = await get_user_by_username(form_data.username, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if verify_password(form_data.password, user.hashed_password):
        access_token = create_access_token({"username": user.username})
        return JSONResponse(status_code=200, content={"access_token": access_token, "token_type": "bearer"})

    raise HTTPException(
        status_code=400,
        detail="Incorrect username or password"
    )

@router.get("/user_commands")
async def get_user_commands(user_id: int, db: Database = Depends(get_db)):
    user = await db.fetch_one(select(User).where(User.id == user_id))
    return user