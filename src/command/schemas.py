from pydantic import BaseModel

class CommandCreate(BaseModel):
    name: str
    description: str