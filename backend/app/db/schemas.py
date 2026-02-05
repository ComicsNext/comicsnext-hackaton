# data/schemas.py
from pydantic import BaseModel
from datetime import date, datetime


# ---------------------------
# USUARIOS
# ---------------------------

class UsuarioBase(BaseModel):
    user_nombre: str
    user_mail: str
    user_genero: str
    user_fecha_naci: date
    role_nombre: str = "user"


class UsuarioCreate(UsuarioBase):
    user_password: str


class UsuarioRead(UsuarioBase):
    user_id: int

    class Config:
        orm_mode = True




# ---------------------------
# RESEÑAS
# ---------------------------

class ResenyaBase(BaseModel):
    user_id: int
    item_id: int
    nombre_tabla: str
    texto_resenya: str | None = None
    valoracion: int 

class ResenyaCreate(ResenyaBase):
    pass


class ResenyaRead(ResenyaBase):
    resenya_id: int
    fecha_resenya: datetime | None = None

    class Config:
        from_attributes = True


# ---------------------------
# MANGA
# ---------------------------

class MangaBase(BaseModel):
    Manga_series: str
    Author_s: str
    Publisher: str
    Demographic: str
    No_of_collected_volumes: int
    Serialized: str
    Approximate_sales_in_million_s: float
    Average_sales_per_volume_in_million_s: float


class MangaRead(MangaBase):
    manga_id: int

    class Config:
        orm_mode = True


# ---------------------------
# MARVEL
# ---------------------------

class MarvelBase(BaseModel):
    comic_name: str
    active_years: str
    issue_title: str
    publish_date: date | None = None
    issue_description: str
    penciler: str
    writer: str
    cover_artist: str
    Imprint: str
    Format: str
    Rating: str
    Price: str


class MarvelRead(MarvelBase):
    marvel_id: int

    class Config:
        orm_mode = True
