from typing import Literal

from pydantic import BaseModel, Field
from starlette import status


class CommandBase(BaseModel):

    name: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=255)

class CommandRead(CommandBase):
    pass

class CommandReadResponse(CommandBase):
    id: int = Field(gt=0)
    created_by: str

class CommandCreate(CommandBase):
    pass

class CommandCreateResponse(CommandBase):
    status_code: Literal[
        status.HTTP_201_CREATED,
    ]

class CommandUpdate(CommandBase):
    pass