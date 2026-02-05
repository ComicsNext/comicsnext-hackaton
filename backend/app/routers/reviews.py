from fastapi import APIRouter, Depends
from typing import List

from app.db.database import get_db
from app.db.schemas import ReviewCreate, ReviewOut
from app.services.review_service import (
    create_review,
    get_reviews_by_comic,
)

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)


@router.post("", response_model=ReviewOut)
def add_review(
    review: ReviewCreate,
    db=Depends(get_db),
):
    return create_review(db, review)


@router.get("", response_model=List[ReviewOut])
def list_reviews(
    comic_id: int,
    db=Depends(get_db),
):
    return get_reviews_by_comic(db, comic_id)
