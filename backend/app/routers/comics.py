from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db.schemas import MarvelOut , MangaOut
from app.db.database import get_db
from app.services.comic_service import ( 
    get_full_catalog,
    get_marvel,
    get_manga,
    get_marvel_by_id,
    get_manga_by_id,
    get_marvel_filter,
    get_manga_filter,
    
    
)

router = APIRouter(
    prefix="/comics",
    tags=["Comics"],
)

@router.get("")
def list_comics(db=Depends(get_db)):
    return get_full_catalog(db)

@router.get("/marvel" , response_model=List[MarvelOut] )
def list_comics_marvel(db=Depends(get_db)):
    return get_marvel(db)



@router.get("/filter/marvel" , response_model=List[MarvelOut] )
def list_marvel_filter(
    writer: str | None = None,
    penciler: str | None = None,
    rating: str | None = None,
    imprint: str | None = None,
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=50, description="Resultados por página"),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * size

    return get_marvel_filter(
        db=db,
        writer=writer,
        penciler=penciler,
        rating=rating,
        imprint=imprint,
        skip=skip,
        limit=size,
    )

@router.get("/marvel/{marvel_id}")
def get_comic_marvel(
    marvel_id: int,
    db=Depends(get_db),
):
    marvel = get_marvel_by_id(db, marvel_id)

    if not marvel:
        raise HTTPException(status_code=404, detail="Manga not found")

    return marvel


@router.get("/manga" , response_model=List[MangaOut] )
def list_comics_manga(db=Depends(get_db)):
    return get_manga(db)

@router.get("/filter/manga", response_model=List[MangaOut])
def list_manga_filter(
    author: str | None = None,
    publisher: str | None = None,
    demographic: str | None = None,
    serialized: str | None = None,
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=50, description="Resultados por página"),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * size

    return get_manga_filter(
        db=db,
        author=author,
        publisher=publisher,
        demographic=demographic,
        serialized=serialized,
        skip=skip,
        limit=size,
    )


@router.get("/manga/{manga_id}")
def get_comic_manga(
    manga_id: int,
    db=Depends(get_db),
):
    manga = get_manga_by_id(db, manga_id)

    if not manga:
        raise HTTPException(status_code=404, detail="Manga not found")

    return manga
