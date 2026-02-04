from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_nombre = Column(String, nullable=False)
    user_mail = Column(String, unique=True, index=True, nullable=False)
    user_password = Column(String, nullable=False)
    user_genero = Column(String)
    user_fecha_naci = Column(Date)

    reviews = relationship("Review", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")

class Comic(Base):
    __tablename__ = "comics"

    id = Column(Integer, primary_key=True, index=True)
    Name = Column(String, nullable=False)
    Author = Column(String)
    Publisher = Column(String)
    Demographic = Column(String)
    Year_of_release = Column(Integer)

    reviews = relationship("Review", back_populates="comic")
    favorites = relationship("Favorite", back_populates="comic")


class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    comic_id = Column(Integer, ForeignKey("comics.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)

    comic = relationship("Comic", back_populates="reviews")
    user = relationship("User", back_populates="reviews")


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    comic_id = Column(Integer, ForeignKey("comics.id"), nullable=False)

    user = relationship("User", back_populates="favorites")
    comic = relationship("Comic", back_populates="favorites")
