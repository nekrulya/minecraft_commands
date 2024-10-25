from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import RedirectResponse
from starlette.status import HTTP_301_MOVED_PERMANENTLY

from backend.src.config import REACT_IP_ADDR, IP_ADDR_WORK

from backend.src.auth.router import router as router_auth
from backend.src.command.router import router as router_command
from backend.src.database import Base, engine

from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Minecraft command"
)

Base.metadata.create_all(engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

# Указываем директорию с шаблонами
templates = Jinja2Templates(directory="src/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[REACT_IP_ADDR, 'http://localhost:3000', IP_ADDR_WORK],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/", response_class=RedirectResponse)
async def root(request: Request):
    return RedirectResponse(url="/docs", status_code=HTTP_301_MOVED_PERMANENTLY)


app.include_router(router_auth)

app.include_router(router_command)
