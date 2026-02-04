from sqlalchemy.orm import Session
from typing import List

from app.db import models


def add_favorite(
    db: Session,
    user_id: int,
    comic_id: int,
):
    """
    Marca un cómic como favorito para un usuario.
    """

    favorite = models.Favorite(
        user_id=user_id,
        comic_id=comic_id,
    )

    db.add(favorite)
    db.commit()
    db.refresh(favorite)

    return favorite


def get_favorites_by_user(
    db: Session,
    user_id: int,
):
    """
    Devuelve los cómics favoritos de un usuario.
    """

    return (
        db.query(models.Favorite)
        .filter(models.Favorite.user_id == user_id)
        .all()
    )
