import os
from typing import Optional

import jwt
from datetime import datetime, timedelta

from argon2 import PasswordHasher
from fastapi import HTTPException
from peewee import DoesNotExist

from app.models.user_models import User


class AuthService:
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def __init__(self, db):
        self.db = db
        self.ph = PasswordHasher()

    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        """Create a new JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=self.ALGORITHM)
        return encoded_jwt

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate the user by verifying the username and password."""
        try:
            user = User.get(User.username == username)
            if self.ph.verify(user.password, password):
                return user
        except DoesNotExist:
            return None
        return None

    def verify_token(self, token: str) -> User:
        """Verify a JWT token and return the associated user."""
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except HTTPException as e:
            raise e
        except jwt.PyJWTError:
            raise credentials_exception
        try:

            user = User.get(User.username == username)
            if user is not None:
               return user
        except DoesNotExist as e:
            raise credentials_exception
