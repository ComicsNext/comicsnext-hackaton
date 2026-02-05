from .api_client import get, post

def list_reviews(comic_id: int):
    return get("/reviews", params={"comic_id": comic_id})

def create_review(user_id: int, comic_id: int, texto: str, valoracion: int, nombre_tabla: str):
    data = {
        "user_id": user_id,
        "item_id": comic_id,
        "nombre_tabla": nombre_tabla,
        "texto_resenya": texto,
        "valoracion": valoracion
    }
    return post("/reviews", data)
