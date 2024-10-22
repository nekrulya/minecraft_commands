from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN


class CommandNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail="Command not found")

class CommandEmptyNameError(HTTPException):
    def __init__(self):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail="Command name cannot be empty")

class CommandEmptyDescriptionError(HTTPException):
    def __init__(self):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail="Command description cannot be empty")

class CommandNameIsTakenError(HTTPException):
    def __init__(self):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail="Command name is taken")

class CommandForbiddenActionError(HTTPException):
    def __init__(self):
        super().__init__(status_code=HTTP_403_FORBIDDEN, detail="You do not have permission to perform this action")

class CommandNameError(HTTPException):
    def __init__(self):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail="Illegal command name")