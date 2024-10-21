from typing import Dict

import bcrypt
from databases import Database
from fastapi import HTTPException
from sqlalchemy import insert, select

from src.auth.models import User

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

async def create_user(username: str, password: str, db: Database) -> None:
    hashed_password = hash_password(password)
    query = insert(User).values(username=username, hashed_password=hashed_password)
    await db.execute(query)


async def get_user_by_username(username: str, db: Database) -> User:
    query = select(User).where(User.username == username)
    user = await db.fetch_one(query)

    return user

def get_user_dict(user) -> Dict[str, str]:
    user_dict_new = {}
    for key in user:
        if key != "hashed_password":
            user_dict_new[key] = user[key]
    return user_dict_new
