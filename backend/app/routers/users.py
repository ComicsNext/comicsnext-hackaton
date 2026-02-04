from fastapi import APIRouter, Depends
from typing import List

from app.db.database import get_db
from app.db.schemas import FavoriteCreate, FavoriteOut
from app.services.user_service import (
    add_favorite,
    get_favorites_by_user,
)

router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"],
)


@router.post("", response_model=FavoriteOut)
def create_favorite(
    favorite: FavoriteCreate,
    db=Depends(get_db),
):
    return add_favorite(
        db,
        user_id=favorite.user_id,
        comic_id=favorite.comic_id,
    )


@router.get("", response_model=List[FavoriteOut])
def list_favorites(
    user_id: int,
    db=Depends(get_db),
):
    return get_favorites_by_user(db, user_id)
