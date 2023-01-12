from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

import database
import schemas
import utils
import crud

router = APIRouter(prefix='/user', tags=['User'])


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)) -> schemas.UserResponse:
    user.password = utils.hash_password(user.password)
    exist_email = crud.get_by_email(user.email, db)
    if exist_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"email '{user.email}' is already registered")
    return crud.create_user(user, db)


@router.get('/{user_id}', response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(database.get_db)) -> schemas.UserResponse:
    user = crud.get_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id '{user_id}' was not found")
    return user
