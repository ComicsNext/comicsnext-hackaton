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
    Obtiene cómics con filtros basados en la tabla comics.
    """

    query = db.query(models.Comic)

    if genre:
        query = query.filter(models.Comic.Demographic == genre)

    if author:
        query = query.filter(models.Comic.Author == author)

    if publisher:
        query = query.filter(models.Comic.Publisher == publisher)

    if year:
        query = query.filter(models.Comic.Year_of_release == year)

    return query.offset(skip).limit(limit).all()


def get_comic_by_id(
    db: Session,
    comic_id: int,
):
    """
    Devuelve un cómic por su ID.
    """

    return (
        db.query(models.Comic)
        .filter(models.Comic.id == comic_id)
        .first()
    )
