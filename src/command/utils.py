from databases import Database
from sqlalchemy import select

from src.auth.exceptions import UserNotFound
from src.auth.models import User
from src.auth.utils import get_user_by_id
from src.command.models import Command


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

async def get_command_by_name(name: str, db: Database):
    name = name.lower().strip()
    query = select(Command).where(Command.name == name)
    command = await db.fetch_one(query)
    return command

async def get_commands_by_user_id(user_id: int, db: Database):
    query = (
        select(Command)
        .where(Command.created_by == user_id)
        .join(User)
        .add_columns(User.username.label('created_by'))
    )
    commands = await db.fetch_all(query)
    return commands