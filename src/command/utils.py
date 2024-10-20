from databases import Database
from sqlalchemy import select

from src.auth.models import User
from src.command.models import Command
from src.database import database


async def get_command_by_id(command_id: int, db: Database, username=False):
    if username:
        query = (
            select(Command)
            .where(Command.id == command_id)
            .join(User)
            .add_columns(User.username.label('created_by'))
        )
    else:
        query = select(Command).where(Command.id == command_id)

    command = await db.fetch_one(query)
    return command

async def get_command_by_name(name: str):
    name = name.lower().strip()
    query = select(Command).where(Command.name == name)
    command = await database.fetch_one(query)
    return command