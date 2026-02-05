import time
from fastapi import APIRouter, HTTPException

from app.schemas.ai import (
    RecommendRequest,
    RecommendResponse,
    SummarizeRequest,
    SummarizeResponse,
    AnalyzeReviewRequest,
    AnalyzeReviewResponse,
)
from app.services.ai_service import recommend, summarize, analyze_review
from app.utils.checkpoints import save_checkpoint

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/recommend", response_model=RecommendResponse)
async def ai_recommend(body: RecommendRequest):
    t0 = time.time()
    recs = await recommend(body.user_profile, body.candidates, body.top_k, history=body.history)
    dt_ms = int((time.time() - t0) * 1000)

    payload = {
        "endpoint": "/ai/recommend",
        "latency_ms": dt_ms,
        "input": body.model_dump(),
        "output": {"top_k": body.top_k, "recommendations": [r.model_dump() for r in recs]},
    }
    path = save_checkpoint("recommend", payload)

    return RecommendResponse(top_k=body.top_k, recommendations=recs)


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