from typing import Literal

from pydantic import BaseModel, Field
from starlette.responses import JSONResponse


class CommandBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=255)

class CommandRead(CommandBase):
    pass

class CommandReadResponse(CommandBase):
    id: int = Field(gt=0)
    created_by: str | int

class CommandCreate(CommandBase):
    pass

class CommandCreateResponse(CommandBase):
    pass

class CommandUpdate(CommandBase):
    pass

class CommandUpdateResponse(CommandBase):
    pass

class CommandDelete(CommandBase):
    pass

class CommandDeleteResponse(CommandBase):
    pass