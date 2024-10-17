import os

from fastapi import FastAPI, Depends, HTTPException
from databases import Database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, MetaData
from src.auth.router import router as router_auth
from src.command.router import router as router_command
from src.database import Base, engine

app = FastAPI(
    title="Minecraft command"
)

Base.metadata.create_all(engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}



app.include_router(router_auth)

app.include_router(router_command)
