from .api_client import post

def register_user(nombre, email, genero, fecha_naci, password, role="user"):
    data = {
        "user_nombre": nombre,
        "user_mail": email,
        "user_genero": genero,
        "user_fecha_naci": fecha_naci,
        "user_password": password,
        "role_nombre": role
    }
    return post("/auth/register", data)

def login_user(email, password):
    data = {"email": email, "password": password}
    return post("/auth/login", data)
