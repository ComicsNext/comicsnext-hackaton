# main.py
import sys
import os


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) 
sys.path.append(ROOT_DIR)


from backend.app.db import models

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.db.database import get_db
from backend.app.db import schemas


# Añadir la raíz del proyecto al path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


app = FastAPI()

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT * FROM tipos_comic"))
        rows = result.fetchall()

        # Convertir cada fila en un diccionario
        data = [dict(row._mapping) for row in rows]

        return {"conexion": "OK", "resultado": data}

    except Exception as e:
        return {"conexion": "ERROR", "detalle": str(e)}
