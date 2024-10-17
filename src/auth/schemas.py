from typing import Optional

from pydantic import BaseModel


class UserRead(BaseModel):
    username: str

class UserCreate(BaseModel):
    username: str
    password: str