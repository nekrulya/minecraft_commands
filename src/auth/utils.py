import bcrypt
from sqlalchemy import insert, select

from src.auth.models import User
from src.database import database

from src.auth.token_util import create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

async def create_user(username: str, password: str) -> None:
    hashed_password = hash_password(password)
    query = insert(User).values(username=username, hashed_password=hashed_password)
    await database.execute(query)


async def get_user_by_username(username: str) -> User:
    query = select(User).where(User.username == username)
    user = await database.fetch_one(query)
    return user

