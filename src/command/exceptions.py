from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND


class CommandNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail="Command not found")