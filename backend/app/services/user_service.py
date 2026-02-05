from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException , status
from app.db.schemas import UserCreate
from datetime import timedelta
from app.db import models
from app.core.security import (
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    hash_password
)


def create_user(db: Session, user: UserCreate):
    exists = (
        db.query(models.User)
        .filter(models.User.user_mail == user.user_mail)
        .first()
    )

    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        user_nombre=user.user_nombre,
        user_mail=user.user_mail,
        user_password=hash_password(user.password),
        user_fecha_naci = user.user_fecha_naci,
        role_nombre = user.user_role,
        user_genero=user.user_genero,
        
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, identifier: str, password: str) -> str:
    """
    Autentica por email o por user_id.
    """

    if identifier.isdigit():
        user = (
            db.query(models.User)
            .filter(models.User.user_id == int(identifier))
            .first()
        )
    else:
        user = (
            db.query(models.User)
            .filter(models.User.user_mail == identifier)
            .first()
        )

    if not user or not verify_password(password, user.user_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": str(user.user_id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return token

def get_users(db: Session) -> List[models.User]:
    """
    Devuelve todos los usuarios.
    """
    return db.query(models.User).all()

def delete_user(db: Session, user_id: int) -> None:
    """
    Elimina el usuario autenticado.
    """

    user = (
        db.query(models.User)
        .filter(models.User.user_id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    db.delete(user)
    db.commit()