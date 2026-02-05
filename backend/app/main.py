from app.routers import comics, reviews, users, ai
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import Base, engine,get_db
from app.db import models 
import sys
import os
 
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOT_DIR)
 
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ComicsNext API",
    description="API REST para cómics, reviews y favoritos",
    version="1.0.0",
)

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 4 ")).fetchone()
    return {"ok": True, "result": result[0]}

app.include_router(ai.router)
app.include_router(comics.router)
app.include_router(reviews.router)
app.include_router(users.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok"}
