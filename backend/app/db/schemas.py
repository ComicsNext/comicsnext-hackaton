from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Optional

class UserBase(BaseModel):
    user_nombre: str
    user_mail: EmailStr
    user_genero: Optional[str]
    user_fecha_naci: Optional[date]

class UserOut(UserBase):
    user_id: int

    class Config:
        orm_mode = True

class ComicOut(BaseModel):
    id: int
    Name: str
    Author: Optional[str]
    Publisher: Optional[str]
    Demographic: Optional[str]
    Year_of_release: Optional[int]

    class Config:
        orm_mode = True

class ReviewCreate(BaseModel):
    comic_id: int
    user_id: int
    rating: int = Field(ge=1, le=5)
    comment: Optional[str]

class ReviewOut(ReviewCreate):
    review_id: int

    class Config:
        orm_mode = True

class FavoriteCreate(BaseModel):
    user_id: int
    comic_id: int

class FavoriteOut(FavoriteCreate):
    id: int

    class Config:
        orm_mode = True
