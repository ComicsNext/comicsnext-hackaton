from .api_client import post, get
import requests

def register_user(nombre, email, genero, fecha_naci, password, role="user"):
    data = {
        "user_nombre": nombre,
        "user_mail": email,
        "password": password,
        "user_genero": genero,
        "role_nombre": role,
        "user_fecha_naci": str(fecha_naci)
    }
    return post("/user/create", data)


def login_user(email, password):
    data = {
        "username": email,
        "password": password
    }
    r = requests.post("http://localhost:8000/user/login", data=data) # <-- data, no json r.raise_for_status()
    r.raise_for_status()
    return r.json()

def list_users():
    return get("/user")

def delete_user(user_id):
    data = {"id": user_id}
    return post("/user/delete", data)
