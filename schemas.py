from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, validator
from pydantic.types import constr
from fastapi import HTTPException, status

from utils import check_password, verify_email


class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)

    @validator('password')
    def validate_password(cls, value):
        if not check_password(value):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail='password must contain at least 8 characters, one uppercase letter, '
                                       'one lowercase letter, one number and one special character')
        return value

    @validator('email')
    def validate_email(cls, value):
        if not verify_email(value):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail='email is at risk, try another email')
        return value


class UserResponse(OurBaseModel):
    email: EmailStr


class Token(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None
