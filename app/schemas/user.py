from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated


class UserSignUp(BaseModel):
    full_name: str
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=6)]


class UserSignUpSuccess(BaseModel):
    message: str


class UserLogin(BaseModel):
    email: EmailStr
    password: Annotated[str, StringConstraints()]


class UserLoginSuccess(BaseModel):
    message: str
    access_token: str
