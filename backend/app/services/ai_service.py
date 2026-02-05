import os
import time
from typing import List, Optional, Dict, Any

from app.schemas.ai import (
    ComicCandidate,
    Recommendation,
    SummarizeResponse,
    AnalyzeReviewResponse,
)

import sys
from pathlib import Path

# Añadir raíz del repo al PYTHONPATH para poder importar /rag
ROOT = Path(__file__).resolve().parents[3]  # backend/app/services/ai_service.py -> repo root
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
    
from rag.rag_pipeline import rag_recommend

# ----------------------------
# Config simple por ENV
# ----------------------------
RAG_ENABLED = os.getenv("RAG_ENABLED", "false").lower() == "true"
print("DEBUG RAG_ENABLED =", RAG_ENABLED, "RAW=", os.getenv("RAG_ENABLED"))
AI_PROVIDER = os.getenv("AI_PROVIDER", "mock").lower()  # "openai" o "mock"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def _mock_recommend(user_profile: str, candidates: List[ComicCandidate], top_k: int) -> List[Recommendation]:
    """
    Heurística sencilla (hackathon): scoring por coincidencia de palabras con géneros/título/sinopsis.
    """
    profile = (user_profile or "").lower()

    scored = []
    for c in candidates:
        text = f"{c.title} {(c.synopsis or '')} {' '.join(c.genres)}".lower()

        # score base
        score = 0.2

        # bonus por coincidencia de tokens simples
        for token in set(profile.split()):
            if len(token) < 4:
                continue
            if token in text:
                score += 0.12

        # normaliza
        score = min(score, 0.99)

        reason = "Recomendado por afinidad con tus gustos (coincidencias en género/temática)."
        scored.append((score, Recommendation(comic_id=c.comic_id, score=score, reason=reason)))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [rec for _, rec in scored[:top_k]]


def _mock_summarize(title: str, synopsis: str, max_words: int) -> SummarizeResponse:
    words = synopsis.strip().split()
    trimmed = " ".join(words[:max_words])
    if len(words) > max_words:
        trimmed += "…"
    return SummarizeResponse(summary=f"{title}: {trimmed}")


def _mock_analyze(review_text: str) -> AnalyzeReviewResponse:
    t = (review_text or "").lower()

    positives = ["increíble", "genial", "brutal", "me encantó", "obra maestra", "buenísimo"]
    negatives = ["malo", "aburrido", "horrible", "no me gustó", "decepcionante", "flojo"]

    p = sum(1 for w in positives if w in t)
    n = sum(1 for w in negatives if w in t)

    if p > n:
        sentiment = "positive"
    elif n > p:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    tags = []
    if "arte" in t or "dibujo" in t:
        tags.append("art")
    if "historia" in t or "trama" in t:
        tags.append("story")
    if "personaje" in t:
        tags.append("characters")

    short_reason = "Clasificación aproximada (heurística por palabras clave)."
    return AnalyzeReviewResponse(sentiment=sentiment, tags=tags, short_reason=short_reason)


async def recommend(user_profile: str, candidates: List[ComicCandidate], top_k: int, history: Optional[List[Dict[str, Any]]] = None,) -> List[Recommendation]:
    """
    Devuelve recomendaciones con score + reason.
    """
    # 0) Intentar RAG primero
    if RAG_ENABLED:
        try:
            rag_out = rag_recommend(
                user_profile={"text": user_profile},
                candidates=[c.model_dump() for c in candidates],
                top_k=top_k,
                history=history,
            )

            recs = [Recommendation(**item) for item in rag_out[:top_k]]
            if recs:
                return recs

        except Exception as e:
            print("RAG failed:", repr(e))
    if AI_PROVIDER == "openai":
        # Implementación OpenAI opcional (para hackathon, mantenemos fallback si falta key)
        try:
            from openai import AsyncOpenAI  # type: ignore
            if not OPENAI_API_KEY:
                return _mock_recommend(user_profile, candidates, top_k)

            client = AsyncOpenAI(api_key=OPENAI_API_KEY)

            # Mandamos candidatos resumidos para no gastar tokens
            compact = [
                {"comic_id": c.comic_id, "title": c.title, "genres": c.genres, "synopsis": (c.synopsis or "")[:300]}
                for c in candidates
            ]

            prompt = (
                "Eres un recomendador de cómics. "
                "Dado un perfil de usuario y una lista de candidatos, devuelve TOP recomendaciones "
                "en JSON con: comic_id, score (0-1), reason (1 frase). "
                "No inventes cómics fuera de la lista.\n\n"
                f"USER_PROFILE: {user_profile}\n\n"
                f"CANDIDATES: {compact}\n\n"
                f"TOP_K: {top_k}\n"
                "OUTPUT: JSON array."
            )

            resp = await client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            content = (resp.choices[0].message.content or "").strip()

            # parse naive (si viene mal, fallback)
            import json
            arr = json.loads(content)

            recs: List[Recommendation] = []
            for item in arr[:top_k]:
                recs.append(
                    Recommendation(
                        comic_id=int(item["comic_id"]),
                        score=float(item.get("score", 0.5)),
                        reason=str(item.get("reason", ""))[:240],
                    )
                )
            return recs

        except Exception:
            return _mock_recommend(user_profile, candidates, top_k)

    # default mock
    return _mock_recommend(user_profile, candidates, top_k)

async def summarize(title: str, synopsis: str, max_words: int) -> SummarizeResponse:
    if AI_PROVIDER == "openai":
        try:
            from openai import AsyncOpenAI  # type: ignore
            if not OPENAI_API_KEY:
                return _mock_summarize(title, synopsis, max_words)

            client = AsyncOpenAI(api_key=OPENAI_API_KEY)
            prompt = (
                f"Resume en español en máximo {max_words} palabras. "
                "Tono neutro, sin spoilers fuertes.\n\n"
                f"TITULO: {title}\nSINOPSIS: {synopsis}"
            )

            resp = await client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            text = (resp.choices[0].message.content or "").strip()
            return SummarizeResponse(summary=text)

        except Exception:
            return _mock_summarize(title, synopsis, max_words)

    return _mock_summarize(title, synopsis, max_words)


async def analyze_review(review_text: str) -> AnalyzeReviewResponse:
    if AI_PROVIDER == "openai":
        try:
            from openai import AsyncOpenAI  # type: ignore
            if not OPENAI_API_KEY:
                return _mock_analyze(review_text)

            client = AsyncOpenAI(api_key=OPENAI_API_KEY)
            prompt = (
                "Analiza el sentimiento de la reseña (positive/neutral/negative) "
                "y saca 2-4 tags cortos. Devuelve SOLO JSON con campos: sentiment, tags, short_reason.\n\n"
                f"RESEÑA: {review_text}"
            )

            resp = await client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            content = (resp.choices[0].message.content or "").strip()

            import json
            obj = json.loads(content)
            return AnalyzeReviewResponse(
                sentiment=str(obj.get("sentiment", "neutral")),
                tags=list(obj.get("tags", []))[:6],
                short_reason=str(obj.get("short_reason", ""))[:240],
            )

        except Exception:
            return _mock_analyze(review_text)

    return _mock_analyze(review_text)