from fastapi import FastAPI

from app.routers import comics, reviews, users

app = FastAPI(
    title="ComicsNext API",
    description="API REST para cómics, reviews y favoritos",
    version="1.0.0",
)

app.include_router(comics.router)
app.include_router(reviews.router)
app.include_router(users.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok"}
