from typing import AsyncGenerator

from sqlalchemy.orm import declarative_base

from src.config import DATABASE_URL
from databases import Database

from sqlalchemy import MetaData, create_engine

# Асинхронное подключение к базе данных
database = Database(DATABASE_URL)

# Настройка SQLAlchemy для создания моделей и таблиц
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()
