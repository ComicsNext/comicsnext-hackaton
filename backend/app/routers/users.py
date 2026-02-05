from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas import UserCreate, UserOut, UserDelete
from app.services.user_service import create_user ,authenticate_user, delete_user, get_users
from fastapi.security import OAuth2PasswordRequestForm
from app.core.dependencies import admin_required

router = APIRouter(prefix="/user", tags=["User"])

@router.get("", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    return get_users(db)

@router.post("/create", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    token = authenticate_user(
        db=db,
        identifier=form_data.username,
        password=form_data.password,
    )
    return {
        "access_token": token,
        "token_type": "bearer",
    }



@router.post("/delete", response_model=UserDelete, dependencies=[Depends(admin_required)])
def delete_user(user: UserDelete, db: Session = Depends(get_db)):
    return delete_user(db, user)
