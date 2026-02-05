from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import models

from sqlalchemy.orm import Session
from typing import List
from app.db import models


def get_full_catalog(db: Session):
    """
    Devuelve todo el catálogo: manga + marvel.
    """

    manga = db.query(models.Manga).limit(500).all()
    marvel = db.query(models.Marvel).limit(500).all()

    comics = manga + marvel

    return comics




def get_marvel(db: Session):
    """
    Devuelve todo el catálogo: manga + marvel.
    """
    return db.query(models.Marvel).filter(100).all()

    

def get_manga(db: Session):
    """
    Devuelve todo el catálogo: manga + marvel.
    """
    return db.query(models.Manga).all()
    

def get_marvel_by_id(
    db: Session,
    marvel_id: int,
):
    """
    Devuelve un cómic Marvel por su ID.
    """
    return (
        db.query(models.Marvel)
        .filter(models.Marvel.marvel_id == marvel_id)
        .first()
    )


def get_manga_by_id(
    db: Session,
    manga_id: int,
):
    """
    Devuelve un Manga por su ID.
    """
    return (
        db.query(models.Manga)
        .filter(models.Manga.manga_id == manga_id)
        .first()
    )


def get_marvel_filter(
    db: Session,
    writer: Optional[str] = None,
    penciler: Optional[str] = None,
    rating: Optional[str] = None,
    imprint: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[models.Marvel]:
    """
    Obtiene cómics Marvel aplicando filtros opcionales.
    """

    query = db.query(models.Marvel)

    if writer:
        query = query.filter(models.Marvel.writer == writer)

    if penciler:
        query = query.filter(models.Marvel.penciler == penciler)

    if rating:
        query = query.filter(models.Marvel.Rating == rating)

    if imprint:
        query = query.filter(models.Marvel.Imprint == imprint)

    return query.order_by(models.Marvel.marvel_id).offset(skip).limit(limit).all() # 👈 OBLIGATORIO EN AZURE


def get_manga_filter(
    db: Session,
    author: Optional[str] = None,
    publisher: Optional[str] = None,
    demographic: Optional[str] = None,
    serialized: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[models.Manga]:
    """
    Obtiene Mangas aplicando filtros opcionales.
    """

    query = db.query(models.Manga)

    if author:
        query = query.filter(models.Manga.Author_s == author)

    if publisher:
        query = query.filter(models.Manga.Publisher == publisher)

    if demographic:
        query = query.filter(models.Manga.Demographic == demographic)

    if serialized:
        query = query.filter(models.Manga.Serialized == serialized)

    return query.order_by(models.Manga.manga_id).offset(skip).limit(limit).all() 


