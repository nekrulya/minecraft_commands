from typing import AsyncGenerator

from sqlalchemy.orm import declarative_base

from backend.src.config import DATABASE_URL
from databases import Database

from sqlalchemy import create_engine

# Асинхронное подключение к базе данных
database = Database(DATABASE_URL)

# Настройка SQLAlchemy для создания моделей и таблиц
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()

async def get_db() -> AsyncGenerator[Database, None]:
    try:
        # Подключаемся к базе данных
        await database.connect()
        yield database  # Передаём подключение для использования
    finally:
        # Отключаемся от базы данных
        await database.disconnect()
