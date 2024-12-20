from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

class UserRead(UserBase):
    pass

class UserReadResponse(UserBase):
    id: int = Field(..., gt=0)

class UserCreate(UserBase):
    password: str = Field(..., min_length=4, max_length=128)

class UserCreateResponse(UserBase):
    pass