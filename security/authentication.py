from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated

from models.user_models.new_user import NewUser as User
from models.token_models.token_data import TokenData
from services.security_service import SecurityService
from repositories.user_repository import UserRepository

import os

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Authenticate:
    @staticmethod
    async def authenticate_user(username: str, password: str):
        user = await UserRepository.get_by_username(username)
        if not user:
            return False
        if not await SecurityService.verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = await UserRepository.get_by_username(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    @staticmethod
    async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)],
    ):
        awaited_current_user = await current_user
        if awaited_current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return awaited_current_user

    @staticmethod
    def get_access_token_expire_minutes():
        time = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
        return int(time)
