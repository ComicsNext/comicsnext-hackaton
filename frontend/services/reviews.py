from .api_client import get, post

def add_resenya(item_id, nombre_tabla, texto_resenya, valoracion):
    data = {
        "item_id": item_id,
        "nombre_tabla": nombre_tabla,
        "texto_resenya": texto_resenya,
        "valoracion": valoracion
    }
    return post("/resenyas", data=data)

def list_resenyas(item_id, nombre_tabla):
    params = {
        "item_id": item_id,
        "nombre_tabla": nombre_tabla
    }
    return get("/resenyas/list", params=params)

def list_all_resenyas():
    return get("/resenyas/list_all")

def delete_resenya(resenya_id):
    params = {"resenya_id": resenya_id}
    return get("/resenyas/delete", params=params)

