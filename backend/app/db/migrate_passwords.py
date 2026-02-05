from backend.app.db.database import SessionLocal
from backend.app.db import models
from backend.app.db.security import hash_password

db = SessionLocal()

usuarios = db.query(models.Usuario).all()

for u in usuarios:
    if u.user_password is None:
        continue

    try:
        # Intentar interpretar el binario como texto (solo funciona si era CONVERT(VARBINARY, '12345'))
        original = u.user_password.decode("utf-8")

        # Si la contraseña decodificada es muy corta, asumimos que era texto plano
        if len(original) < 50:  
            hashed = hash_password(original)
            u.user_password = hashed
            print(f"Usuario {u.user_mail}: migrado")
        else:
            print(f"Usuario {u.user_mail}: ya tenía hash seguro, no se toca")

    except UnicodeDecodeError:
        # No se puede decodificar → ya es hash seguro
        print(f"Usuario {u.user_mail}: ya tenía hash seguro, no se toca")
        continue

db.commit()
db.close()

print("Contraseñas migradas correctamente.")
