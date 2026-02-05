from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.dependencies import get_current_user_id
from app.db.database import get_db
from app.db.schemas import ResenyaCreate, ResenyaOut
from app.services.review_service import (
    create_resenya,
    get_resenya, 
    get_all_resenyas,
    delete_resenya_id
)
router = APIRouter(prefix="/resenyas", tags=["Reseñas"])


@router.post("", response_model=ResenyaCreate)
def add_resenya(
    item_id: int, 
    nombre_tabla : str,
    texto_resenya: str,
    valoracion: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    return create_resenya(db = db,
            texto_resenya=texto_resenya,
            nombre_tabla=nombre_tabla,
            user_id = user_id,
            valoracion = valoracion,
            item_id=item_id)


@router.get("/list", response_model=List[ResenyaOut])
def list_resenya(
    item_id: int,
    nombre_tabla: str = Query(
            examples=["manga"]
            ),
    db: Session = Depends(get_db),
):
    return get_resenya(db, item_id, nombre_tabla)

@router.get("/list_all", response_model=List[ResenyaOut])
def list_all_resenyas(db: Session = Depends(get_db)):
    return get_all_resenyas(db)



@router.get("/delete")
def delete_resenya(
    resenya_id : int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    return delete_resenya_id(db, resenya_id , user_id)
