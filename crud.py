from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

import schemas
import models


def get_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(user_data: schemas.UserCreate, db: Session) -> models.User:
    created_user = models.User(**user_data.dict())
    db.add(created_user)
    db.commit()
    return created_user


def get_by_id(user_id: int, db: Session):
    return db.query(models.User).filter_by(id=user_id).first()


def get_by_username(user_credentials: OAuth2PasswordRequestForm, db: Session):
    return db.query(models.User).filter_by(email=user_credentials.username).first()
