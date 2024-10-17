import os

from fastapi import FastAPI
from databases import Database
from sqlalchemy import create_engine, MetaData

DATABASE_URL = "sqlite:///test.db"

# Асинхронное подключение к базе данных
database = Database(DATABASE_URL)

# Настройка SQLAlchemy для создания моделей и таблиц
metadata = MetaData()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
