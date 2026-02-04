from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List

from app.db.database import get_db
from app.db.schemas import ComicOut
from app.services.comic_service import (
    get_comics,
    get_comic_by_id,
)

router = APIRouter(
    prefix="/comics",
    tags=["Comics"],
)


@router.get("", response_model=List[ComicOut])
def list_comics(
    genre: str | None = None,
    author: str | None = None,
    publisher: str | None = None,
    year: int | None = None,
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=50, description="Resultados por página"),
    db=Depends(get_db),
):
    skip = (page - 1) * size
    limit = size

    return get_comics(
        db=db,
        genre=genre,
        author=author,
        publisher=publisher,
        year=year,
        skip=skip,
        limit=limit,
    )


@router.get("/{comic_id}", response_model=ComicOut)
def get_comic(
    comic_id: int,
    db=Depends(get_db),
):
    comic = get_comic_by_id(db, comic_id)

    if not comic:
        raise HTTPException(status_code=404, detail="Comic not found")

    return comic
