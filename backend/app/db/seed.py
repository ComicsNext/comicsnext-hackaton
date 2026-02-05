# data/seed.py
from database import SessionLocal
from db import models

def seed():
    db = SessionLocal()
    try:
        user = models.Usuario(
            user_nombre="Usuario de prueba",
            user_mail="prueba@example.com", 
            user_genero="Hombre", 
            user_fecha_naci="1990-01-01", 
            user_password=b"12345", 
            role_nombre="user"
        )       
        db.add(user)
        db.commit()
        db.refresh(user)
        print("Usuario creado con ID:", user.id)
    except Exception as e:
        db.rollback()
        print("Error en seed:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed()
