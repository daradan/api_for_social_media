from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

import database
import models
import schemas
import crud
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user/auth')


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire_in = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire_in})
    jwt_str = jwt.encode(to_encode, key=settings.JWT_ENCODE_KEY, algorithm=settings.JWT_ALGORITHM)
    return jwt_str


def verify_access_token(token: str, credential_exception: Exception) -> schemas.TokenData:
    try:
        payload = jwt.decode(token, key=settings.JWT_ENCODE_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        raise credential_exception
    user_id = payload.get('user_id')
    if not user_id:
        raise credential_exception
    return schemas.TokenData(user_id=user_id)


def verify_current_user(token: str = Depends(oauth2_scheme),
                        db: Session = Depends(database.get_db)) -> models.User:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail='Couldn\'t verify credentials',
                                          headers={'WWW-Authenticate': 'Bearer'})
    token_data = verify_access_token(token, credentials_exception)
    user = crud.get_by_id(user_id=int(token_data.user_id), db=db)
    return user
