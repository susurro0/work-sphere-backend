import re
from pydantic import BaseModel, Field, EmailStr, field_validator, constr, ConfigDict, conint


class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    role: str = Field(default='user')


    model_config = ConfigDict()  # Base model configuration

    @field_validator('username')
    def validate_username(cls, value):
        if not re.match(r'^\w+$', value):
            raise ValueError('Username must be a single word without spaces, whitespace, or special characters.')
        if len(value) < 5:
            raise ValueError('Username must be at least 5 characters long.')
        return value

class UserCreate(UserBase):
    password: constr(min_length=8)

    @field_validator('password')
    def validate_password(cls, value):
        if not re.search(r'[A-Z]', value):
            raise ValueError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', value):
            raise ValueError('Password must contain at least one lowercase letter.')
        if not re.search(r'[0-9]', value):
            raise ValueError('Password must contain at least one digit.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError('Password must contain at least one special character.')
        return value

class User(UserBase):
    id: conint(gt=0)

class TokenResponse(UserBase):
    access_token: str
    token_type: str = "bearer"

    @field_validator('access_token')
    def check_access_token(cls, value):
        if not value:
            raise ValueError('Access token cannot be empty.')
        return value

class LoginRequest(BaseModel):
    username: str = Field(..., max_length=50)
    password: constr(min_length=8)

    @field_validator('username')
    def validate_username(cls, value):
        if not re.match(r'^\w+$', value):
            raise ValueError('Username must be a single word without spaces, whitespace, or special characters.')
        if len(value) < 5:
            raise ValueError('Username must be at least 5 characters long.')
        return value

    @field_validator('password')
    def validate_password(cls, value):
        if not re.search(r'[A-Z]', value):
            raise ValueError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', value):
            raise ValueError('Password must contain at least one lowercase letter.')
        if not re.search(r'[0-9]', value):
            raise ValueError('Password must contain at least one digit.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError('Password must contain at least one special character.')
        return value
