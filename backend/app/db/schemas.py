from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional

class UserOut(BaseModel):
    user_id: int
    user_nombre: str
    user_mail: str
    user_genero: str
    user_role: str = Field(alias="role_nombre") # worker | client
    user_fecha_naci: Optional[date] = None  # ✅ Acepta NULL

    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    user_nombre: str
    user_mail: EmailStr
    password: str
    user_genero: str
    user_role: str = Field(alias="role_nombre") # worker | client
    user_fecha_naci: Optional[date] = "2026-02-05"



class UserDelete(BaseModel):
    user_id: str

class MangaOut(BaseModel):
    manga_id: int
    Manga_series: str
    Author_s: str
    Publisher: str
    Demographic: str
    No_of_collected_volumes: int
    Serialized: str
    Approximate_sales_in_million_s: float
    Average_sales_per_volume_in_million_s: float

    model_config = {"from_attributes": True}

class MarvelOut(BaseModel):
    marvel_id: int
    comic_name: str
    active_years: str
    issue_title: str
    publish_date: Optional[date]
    issue_description: str
    penciler: str
    writer: str
    cover_artist: str
    Imprint: str
    Format: str
    Rating: str
    Price: str

    model_config = {"from_attributes": True}


class ResenyaCreate(BaseModel):
    item_id: int
    nombre_tabla: str = Field(example="manga")
    valoracion: Optional[int] = Field(None, ge=1, le=5)
    texto_resenya: Optional[str]


class ResenyaOut(ResenyaCreate):
    user_id : int
    resenya_id: int
    valoracion : int
    model_config = {"from_attributes": True}

class LoginRequest(BaseModel):
    identifier: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
