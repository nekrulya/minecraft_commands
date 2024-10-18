from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette.responses import JSONResponse

from src.auth.schemas import UserCreate
from src.auth.token_util import create_access_token
from src.auth.utils import create_user, get_user_by_username, verify_password

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

@router.get("/{username}")
async def get_user(username: str):
    user = await get_user_by_username(username)
    return user

@router.post("/register")
async def register_user(user: UserCreate):
    existing_user = await get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    await create_user(user.username, user.password)
    return JSONResponse(
        status_code=201,
        content={"username": user.username}
    )

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_username(form_data.username)
    if verify_password(form_data.password, user.hashed_password):
        access_token = create_access_token({"username": user.username})
        return {"access_token": access_token, "token_type": "bearer"}

    return HTTPException(
        status_code=400,
        detail="Incorrect username or password"
    )