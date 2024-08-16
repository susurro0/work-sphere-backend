import re
from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator, conint


class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr = Field(...)  # Validate email

    model_config = ConfigDict()  # Base model configuration

    @field_validator('username')
    def validate_username(cls, value):
        if not re.match(r'^\w+$', value):
            raise ValueError('Username must be a single word without spaces, whitespace, or special characters.')
        return value


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)  # Add a password field for creating a user


class User(UserBase):
    id: conint(gt=0)

    model_config = ConfigDict(from_attributes=True)  # Enables using attributes from ORM models (similar to 'orm_mode')
