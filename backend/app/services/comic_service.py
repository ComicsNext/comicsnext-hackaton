from sqlalchemy.orm import Session
from typing import List

from app.db import models


def get_comics(
    db: Session,
    genre: str | None,
    author: str | None,
    publisher: str | None,
    year: int | None,
    skip: int,
    limit: int,
) -> List[models.Comic]:
    """
    Obtiene lista de cómics con filtros y paginación.
    """

    query = db.query(models.Comic)

    if genre:
        query = query.filter(models.Comic.genre == genre)

    if author:
        query = query.filter(models.Comic.author == author)

    if publisher:
        query = query.filter(models.Comic.publisher == publisher)

    if year:
        query = query.filter(models.Comic.year == year)

    return query.offset(skip).limit(limit).all()

def get_comic_by_id(db: Session, comic_id: int) -> models.Comic | None:
    """
    Devuelve un cómic por ID.
    """
    return (
        db.query(models.Comic)
        .filter(models.Comic.id == comic_id)
        .first()
    )
