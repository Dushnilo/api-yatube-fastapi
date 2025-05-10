from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import EmailStr

from config import settings
from users.models import UsersDAO

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict, token_type: str = 'access'):
    if token_type == 'access':
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    elif token_type == 'refresh':
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    else:
        raise ValueError("Invalid token type. Use 'access' or 'refresh'.")

    to_encode = {'token_type': token_type, 'exp': expire}
    to_encode.update(data)

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY,
                             settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user or not verify_password(password, user.password):
        return None
    return user


async def get_token_payload(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401,
                                          detail='Invalid token.')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
    except JWTError:
        raise credentials_exception

    expire: int = payload.get('exp')
    current_time = datetime.utcnow().timestamp()
    if not expire or expire < current_time:
        raise HTTPException(status_code=401,
                            detail='Token expired.')
    return payload


async def validate_access_token(
        current_user: dict = Depends(get_token_payload)):
    token_type = current_user.get('token_type')
    if token_type != 'access':
        raise HTTPException(
            status_code=401,
            detail='Invalid token type. Expected access token.'
        )
    return current_user
# 
