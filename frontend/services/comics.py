from .api_client import get

# Catálogo completo
def list_all_comics():
    return get("/comics")

# Marvel
def list_marvel():
    return get("/comics/marvel")

def filter_marvel(writer=None, penciler=None, rating=None, imprint=None, page=1, size=10):
    params = {
        "writer": writer,
        "penciler": penciler,
        "rating": rating,
        "imprint": imprint,
        "page": page,
        "size": size
    }
    return get("/comics/filter/marvel", params=params)

def get_marvel_by_id(marvel_id: int):
    return get(f"/comics/marvel/{marvel_id}")

# Manga
def list_manga():
    return get("/comics/manga")

def filter_manga(author=None, publisher=None, demographic=None, serialized=None, page=1, size=10):
    params = {
        "author": author,
        "publisher": publisher,
        "demographic": demographic,
        "serialized": serialized,
        "page": page,
        "size": size
    }
    return get("/comics/filter/manga", params=params)

def get_manga_by_id(manga_id: int):
    return get(f"/comics/manga/{manga_id}")
