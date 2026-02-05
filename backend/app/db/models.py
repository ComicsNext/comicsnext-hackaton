from sqlalchemy import (Column, ForeignKey, Integer, String, Date, DateTime, Float, SmallInteger, VARBINARY, Text)
from app.db.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "usuarios"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_nombre = Column(String(50), nullable=False)
    user_mail = Column(String(50), nullable=False, unique=True, index=True)
    user_genero = Column(
        String(50),
        ForeignKey("usuario_generos.user_genero"),
        nullable=False,
    )
    user_fecha_naci = Column(Date, nullable=False)
    user_password = Column(VARBINARY(64), nullable=True)

    role_nombre = Column(String(20), ForeignKey("roles.role_nombre"), nullable=False)
    
    # relaciones
    genero = relationship("UsuarioGeneros", back_populates="usuarios")
    resenyas = relationship("Resenya", back_populates="usuario")
    role = relationship("Role", back_populates="usuarios")
    
#     __tablename__ = "users"

#     user_id = Column(Integer, primary_key=True, index=True)
#     user_nombre = Column(String(50), nullable=False)
#     user_mail = Column(String(50), nullable=False)
#     user_genero = Column(String(50), nullable=False)
#     user_role = Column(String(50), nullable=False) # worker | client
#     user_fecha_naci = Column(Date, nullable=True)
#     user_password = Column(String(255), nullable=False)



class Manga(Base):
    __tablename__ = "manga"

    manga_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Manga_series = Column(String(50), nullable=False)
    Author_s = Column(String(100), nullable=False)
    Publisher = Column(String(50), nullable=False)
    Demographic = Column(String(50), nullable=False)
    No_of_collected_volumes = Column(SmallInteger, nullable=False)  # tinyint
    Serialized = Column(String(50), nullable=False)
    Approximate_sales_in_million_s = Column(Float, nullable=False)
    Average_sales_per_volume_in_million_s = Column(Float, nullable=False)

# class Manga(Base):
#     __tablename__ = "manga"
#     manga_id = Column(Integer, primary_key=True, index=True)
#     Manga_series = Column(String(50), nullable=False)
#     Author_s = Column(String(100), nullable=False)
#     Publisher = Column(String(50), nullable=False)
#     Demographic = Column(String(50), nullable=False)
#     No_of_collected_volumes = Column(SmallInteger, nullable=False)
#     Serialized = Column(String(50), nullable=False)
#     Approximate_sales_in_million_s = Column(Float, nullable=False)
#     Average_sales_per_volume_in_million_s = Column(Float, nullable=False)


class Marvel(Base):
    __tablename__ = "marvel"

    marvel_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    comic_name = Column(String(300), nullable=False)
    active_years = Column(String(50), nullable=False)
    issue_title = Column(String(100), nullable=False)
    publish_date = Column(Date, nullable=True)
    issue_description = Column(Text, nullable=False)  # nvarchar(max)
    penciler = Column(String(100), nullable=False)
    writer = Column(String(100), nullable=False)
    cover_artist = Column(String(50), nullable=False)
    Imprint = Column(String(50), nullable=False)
    Format = Column(String(50), nullable=False)
    Rating = Column(String(50), nullable=False)
    Price = Column(String(50), nullable=False)

# class Marvel(Base):
#     __tablename__ = "marvel"

#     marvel_id = Column(Integer, primary_key=True, index=True)
#     comic_name = Column(String(300), nullable=False)
#     active_years = Column(String(50), nullable=False)
#     issue_title = Column(String(100), nullable=False)
#     publish_date = Column(Date, nullable=True)
#     issue_description = Column(String, nullable=False)
#     penciler = Column(String(100), nullable=False)
#     writer = Column(String(100), nullable=False)
#     cover_artist = Column(String(100), nullable=False)
#     Imprint = Column(String(50), nullable=False)
#     Format = Column(String(50), nullable=False)
#     Rating = Column(String(50), nullable=False)
#     Price = Column(String(50), nullable=False)



class TiposComic(Base):
    __tablename__ = "tipos_comic"

    nombre_tabla = Column(String(10), primary_key=True)

    # relación con reseñas
    resenyas = relationship("Resenya", back_populates="tipo")


class UsuarioGeneros(Base):
    __tablename__ = "usuario_generos"

    user_genero = Column(String(50), primary_key=True, index=True)

    # relación con usuarios
    usuarios = relationship("User", back_populates="genero")

class Role(Base): 
    __tablename__ = "roles"
    
    role_nombre = Column(String(20), primary_key=True)
    usuarios = relationship("User", back_populates="role")

class Resenya(Base):
    __tablename__ = "resenyas"
    __table_args__ = {"implicit_returning": False}  # 👈 CLAVE

    resenya_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,  # 👈 CLAVE
        index=True,
    )
    user_id = Column(Integer, ForeignKey("usuarios.user_id"), nullable=False)
    item_id = Column(Integer, nullable=False)
    nombre_tabla = Column(
        String(10),
        ForeignKey("tipos_comic.nombre_tabla"),
        nullable=False,
    )
    texto_resenya = Column(Text, nullable=True)  # nvarchar(max)
    fecha_resenya = Column(DateTime, nullable=True)
    valoracion = Column(Integer, nullable=False)


    # relaciones
    usuario = relationship("User", back_populates="resenyas")
    tipo = relationship("TiposComic", back_populates="resenyas")

# class Resenya(Base):
#     __tablename__ = "resenya"

#     resenya_id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, nullable=False)
#     item_id = Column(Integer, nullable=False)
#     nombre_tabla = Column(String(10), nullable=False)  # 'manga' | 'marvel'
#     texto_resenya = Column(String, nullable=True)
#     fecha_resenya = Column(DateTime, nullable=True)