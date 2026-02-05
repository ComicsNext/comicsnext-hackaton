import time
from fastapi import APIRouter, HTTPException ,Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.services.comic_service import get_manga

from app.schemas.ai import (
    RecommendRequest,
    RecommendFromDbRequest,
    RecommendResponse,
    SummarizeRequest,
    SummarizeResponse,
    AnalyzeReviewRequest,
    AnalyzeReviewResponse,
)

from app.services.ai_service import recommend, summarize, analyze_review
from app.utils.checkpoints import save_checkpoint


# Estas funciones las creamos/ajustamos en app/services/db_ai_builders.py
#from app.services.db_ai_builders import fetch_manga_candidates, fetch_history


router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/recommend",  response_model=RecommendResponse)
async def ai_recommend(body: RecommendRequest,  db:Session = Depends(get_db)):
    t0 = time.time()

    mangas = get_manga(db)

    recs = await recommend(body.user_profile, mangas , body.top_k, history=body.history)
    dt_ms = int((time.time() - t0) * 1000)

    payload = {
        "endpoint": "/ai/recommend",
        "latency_ms": dt_ms,
        "input": body.model_dump(),
        "output": {"top_k": body.top_k, "recommendations": [r.model_dump() for r in recs]},
    }
    save_checkpoint("recommend", payload)

    return RecommendResponse(top_k=body.top_k, recommendations=recs)


# @router.post("/recommend_from_db", response_model=RecommendResponse)
# async def ai_recommend_from_db(body: RecommendFromDbRequest):
#     """
#     ✅ Este es el endpoint clave:
#     - NO pasas candidates
#     - candidates + history salen de Azure SQL
#     """
#     try:
#         t0 = time.time()

#         candidates = fetch_manga_candidates(limit=body.candidate_limit)
#         history = fetch_history(user_id=body.user_id) if body.user_id else None

#         recs = await recommend(body.user_profile, candidates, body.top_k, history=history)
#         dt_ms = int((time.time() - t0) * 1000)

#         payload = {
#             "endpoint": "/ai/recommend_from_db",
#             "latency_ms": dt_ms,
#             "input": body.model_dump(),
#             "output": {"top_k": body.top_k, "recommendations": [r.model_dump() for r in recs]},
#         }
#         save_checkpoint("recommend_from_db", payload)

#         return RecommendResponse(top_k=body.top_k, recommendations=recs)

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"DB recommend failed: {repr(e)}")


@router.post("/summarize", response_model=SummarizeResponse)
async def ai_summarize(body: SummarizeRequest):
    t0 = time.time()
    out = await summarize(body.title, body.synopsis, body.max_words)
    dt_ms = int((time.time() - t0) * 1000)

    payload = {
        "endpoint": "/ai/summarize",
        "latency_ms": dt_ms,
        "input": body.model_dump(),
        "output": out.model_dump(),
    }
    save_checkpoint("summarize", payload)
    return out


@router.post("/analyze_review", response_model=AnalyzeReviewResponse)
async def ai_analyze_review(body: AnalyzeReviewRequest):
    t0 = time.time()
    out = await analyze_review(body.review_text)
    dt_ms = int((time.time() - t0) * 1000)

    payload = {
        "endpoint": "/ai/analyze_review",
        "latency_ms": dt_ms,
        "input": {"review_text": body.review_text[:800], "title": body.title},
        "output": out.model_dump(),
    }
    save_checkpoint("analyze_review", payload)
    return out