from .api_client import get

def list_comics(genre=None, author=None, publisher=None, year=None, page=1, size=10):
    params = {
        "genre": genre,
        "author": author,
        "publisher": publisher,
        "year": year,
        "page": page,
        "size": size,
    }
    return get("/comics", params=params)

def get_comic(comic_id: int):
    return get(f"/comics/{comic_id}")
