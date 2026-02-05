from fastapi import HTTPException ,status
from sqlalchemy.orm import Session
from datetime import datetime, UTC
from typing import List
from app.db import models
from app.db.schemas import ResenyaCreate


def create_resenya(
    db: Session,
    user_id: int,
    item_id: int,
    nombre_tabla: str,
    valoracion : int,
    texto_resenya: str | None,
):
    if nombre_tabla not in ("manga", "marvel"):
        raise ValueError("nombre_tabla must be 'manga' or 'marvel'")

    nueva_resenya = models.Resenya(
        user_id=user_id,
        item_id=item_id,
        nombre_tabla=nombre_tabla,
        texto_resenya=texto_resenya,
        valoracion = valoracion,
        fecha_resenya=datetime.now(UTC),
    )

    db.add(nueva_resenya)
    db.commit()
    # db.refresh(nueva_resenya)

    return nueva_resenya


def get_resenya(
    db: Session,
    item_id: int,
    nombre_tabla: str,
) -> List[models.Resenya]:
    """
    Devuelve todas las reseñas de un manga o cómic Marvel.
    """
    return (
        db.query(models.Resenya)
        .filter(
            models.Resenya.item_id == item_id,
            models.Resenya.nombre_tabla == nombre_tabla,
        )
        .order_by(models.Resenya.fecha_resenya.desc())
        .all()
    )

def get_all_resenyas(db: Session,) -> List[models.Resenya]:
    """
    Devuelve todas las reseñas
    """
    return (
        db.query(models.Resenya).all()
    )


def delete_resenya_id(
    db: Session,
    resenya_id: int,
    user_id: int,
):
    """
    Elimina una reseña.
    - El usuario normal solo puede borrar SUS reseñas
    - El admin puede borrar cualquiera
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

    # Usuario normal: solo sus reseñas
    if user.role_nombre == "user":
        resenya = (
            db.query(models.Resenya)
            .filter(
                models.Resenya.resenya_id == resenya_id,
                models.Resenya.user_id == user_id,
            )
            .first()
        )

        if not resenya :
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= f"Esta reseña no pertenece al -- usuario {user.user_nombre} / id : {user_id} --",
        )
    else:
        # Admin: cualquier reseña
        resenya = (
            db.query(models.Resenya)
            .filter(models.Resenya.resenya_id == resenya_id)
            .first()
        )

        if not resenya :
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reseña not found",
            )

    db.delete(resenya)
    db.commit()

    return f"Reseña {resenya_id} Eliminada"
