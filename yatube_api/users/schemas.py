from pydantic import BaseModel, EmailStr
from datetime import datetime


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class SUserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str


class SUserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    date_joined: datetime
    first_name: str | None
    last_name: str | None
    role: str


class SFollowResponse(BaseModel):
    user: str
    following: str


class SCreateTokenResponse(BaseModel):
    access: str
    refresh: str
    token_type: str


class SRefreshTokenResponse(BaseModel):
    access: str
    token_type: str
