from .api_client import get, post

def add_favorite(user_id: int, comic_id: int):
    data = {"user_id": user_id, "comic_id": comic_id}
    return post("/favorites", data)

def list_favorites(user_id: int):
    return get("/favorites", params={"user_id": user_id})
