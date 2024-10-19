from fastapi import HTTPException
from sqlalchemy import select
from starlette import status

from src.command.models import Command
from src.database import database


async def get_command_by_id(command_id: int):
    query = select(Command).where(Command.id == command_id)
    print(command_id)
    command = await database.fetch_one(query)
    print(command)


    # Проверка наличия команды
    if command is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Command not found"
        )

    return command

async def get_command_by_name(name: str):
    query = select(Command).where(Command.name == name)
    command = await database.fetch_one(query)
    return command