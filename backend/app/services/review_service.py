from sqlalchemy.orm import Session
from typing import List

from app.db import models
from app.db.schemas import ReviewCreate

def create_review(
    db: Session,
    review: ReviewCreate,
):
    """
    Crea una reseña asociada a un cómic y un usuario.
    """

    db_review = models.Review(
        comic_id=review.comic_id,
        user_id=review.user_id,
        rating=review.rating,
        comment=review.comment,
    )

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return db_review


def get_reviews_by_comic(
    db: Session,
    comic_id: int,
) -> List[models.Review]:
    """
    Devuelve todas las reseñas de un cómic concreto.
    """

    return (
        db.query(models.Review)
        .filter(models.Review.comic_id == comic_id)
        .all()
    )
