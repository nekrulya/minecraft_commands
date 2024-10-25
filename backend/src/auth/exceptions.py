from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

class UserNotFound(HTTPException):
    def __init__(self, ):
        super().__init__(HTTP_404_NOT_FOUND, "user not found")

class UserAlreadyExists(HTTPException):
    def __init__(self, ):
        super().__init__(HTTP_400_BAD_REQUEST, "user already exists")

class UsernameIncorrectData(HTTPException):
    def __init__(self, ):
        super().__init__(HTTP_400_BAD_REQUEST, "incorrect username or password")