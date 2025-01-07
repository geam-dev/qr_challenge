from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta 

from sqlalchemy.orm import Session 

from src import schemas
from src import db
from src.services import crud, auth

import os


router = APIRouter()

@router.post(
    "/register", 
    tags=["Auth"],
    summary="Register User"
)
def register(
    user: schemas.UserCreate,
    db: Session = Depends(db.get_db)
):
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    db_user = crud.create_user(db=db, email=user.email, password_hash=auth.get_password_hash(user.password))
    return {"email": db_user.email}


@router.post(
    "/token", 
    tags=["Auth"],
    summary="Get Token"
)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(db.get_db)
):
    user = auth.authenticate_user(db=db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = auth.create_access_token(
        data={"sub": user.email}, 
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }