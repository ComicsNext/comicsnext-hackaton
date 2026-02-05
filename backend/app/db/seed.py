from datetime import date, datetime

from app.db.database import SessionLocal, engine, Base
from app.db import models
from app.core.security import hash_password

def seed_db():
    # 🔥 BORRA Y CREA TABLAS (solo desarrollo)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # 👤 USERS
    users = [
        models.User(
            user_nombre="Juan",
            user_mail="juan@comicsnext.com",
            user_genero="Hombre",
            user_fecha_naci=date(1990, 5, 15),
            user_role = "admin",
            user_password=hash_password("12345"),
        ),
        models.User(
            user_nombre="Ana",
            user_mail="ana@comicsnext.com",
            user_genero="Mujer",
            user_fecha_naci=None,
            user_role = "user",
            user_password=hash_password("12345"),
        ),
    ]

    db.add_all(users)
    db.commit()

    manga = [
        models.Manga(
            Manga_series="One Piece",
            Author_s="Eiichiro Oda",
            Publisher="Shueisha",
            Demographic="Shonen",
            No_of_collected_volumes=108,
            Serialized="Yes",
            Approximate_sales_in_million_s=516,
            Average_sales_per_volume_in_million_s=4.8,
        ),
        models.Manga(
            Manga_series="Berserk",
            Author_s="Kentaro Miura",
            Publisher="Hakusensha",
            Demographic="Seinen",
            No_of_collected_volumes=41,
            Serialized="No",
            Approximate_sales_in_million_s=60,
            Average_sales_per_volume_in_million_s=1.4,
        ),
    ]

    db.add_all(manga)
    db.commit()

    marvel = [
        models.Marvel(
            comic_name="Spider-Man",
            active_years="1963–present",
            issue_title="Amazing Fantasy #15",
            publish_date=date(1962, 8, 1),
            issue_description="First appearance of Spider-Man",
            penciler="Steve Ditko",
            writer="Stan Lee",
            cover_artist="Steve Ditko",
            Imprint="Marvel",
            Format="Comic",
            Rating="T",
            Price="$3.99",
        ),
        models.Marvel(
            comic_name="X-Men",
            active_years="1963–present",
            issue_title="X-Men #1",
            publish_date=date(1963, 9, 1),
            issue_description="First appearance of the X-Men",
            penciler="Jack Kirby",
            writer="Stan Lee",
            cover_artist="Jack Kirby",
            Imprint="Marvel",
            Format="Comic",
            Rating="T",
            Price="$4.99",
        ),
    ]

    db.add_all(marvel)
    db.commit()

    resenyas = [
        models.Resenya(
            user_id=1,
            item_id=1,
            nombre_tabla="manga",
            texto_resenya="Una obra maestra absoluta",
            fecha_resenya=datetime.now(),
        ),
        models.Resenya(
            user_id=2,
            item_id=1,
            nombre_tabla="marvel",
            texto_resenya="Un clásico imprescindible",
            fecha_resenya=datetime.now(),
        ),
    ]

    db.add_all(resenyas)
    db.commit()

    db.close()

if __name__ == "__main__":
    seed_db()
    print("✅ Base de datos sembrada correctamente")
