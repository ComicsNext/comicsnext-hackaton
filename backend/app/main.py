from fastapi import FastAPI
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent / ".env"  # backend/app/.env
load_dotenv(dotenv_path=ENV_PATH)
print("DEBUG loaded env from:", ENV_PATH)

# Routers
from app.routers.ai import router as ai_router

app = FastAPI(title="ComicsNext API", version="0.1.0")

# Healthcheck
@app.get("/health")
def health():
    return {"status": "ok"}

# Include routers
app.include_router(ai_router)