import os
from typing import List, Optional, Dict, Any
from app.core.config import settings

from app.schemas.ai import (
    MangaCandidate,
    Recommendation,
    SummarizeResponse,
    AnalyzeReviewResponse,
)

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.rag_pipeline import rag_recommend


RAG_ENABLED = settings.RAG_ENABLED
AI_PROVIDER = settings.AI_PROVIDER
OPENAI_API_KEY = settings.OPENAI_API_KEY
OPENAI_MODEL = settings.OPENAI_MODEL



def _manga_to_rag_candidate(m: MangaCandidate) -> Dict[str, Any]:
    # ✅ Alias para no romper el RAG actual (si esperaba comic_id/title/synopsis/genres)
    return {
        "comic_id": m.manga_id,
        "title": m.Manga_series,
        "synopsis": (
            f"Autor: {m.Author_s}. Editorial: {m.Publisher}. "
            f"Demografía: {m.Demographic}. Serializado en: {m.Serialized}. "
            f"Volúmenes: {m.No_of_collected_volumes}. "
            f"Ventas aprox (M): {m.Approximate_sales_in_million_s}. "
            f"Media por tomo (M): {m.Average_sales_per_volume_in_million_s}."
        ),
        "genres": [m.Demographic],  # aproximación
        "author": m.Author_s,
        "publisher": m.Publisher
        # "extra": m.extra,
    }


def _mock_recommend(user_profile: str, candidates: List[MangaCandidate], top_k: int) -> List[Recommendation]:
    profile = (user_profile or "").lower()

    scored = []
    for c in candidates:
        text = " ".join([
            c.Manga_series,
            c.Author_s,
            c.Publisher,
            c.Demographic,
            c.Serialized,
        ]).lower()

        # --- score base ---
        score = 0.15

        # --- 1) Coincidencia por tokens en campos disponibles ---
        tokens = {t.strip(".,;:¡!¿?()[]\"'").lower() for t in profile.split()}
        tokens = {t for t in tokens if len(t) >= 4}  # evita ruido

        for token in tokens:
            if token in text:
                score += 0.10

        # --- 2) Boost por "intención" (keywords del usuario) ---
        demo = (c.Demographic or "").lower()

        intent_map = {
            "fantasia": ["fantasía", "fantasia", "magia", "dragones", "reinos", "hechic", "místico", "mitolog"],
            "ciencia_ficcion": ["ciencia ficción", "ciencia ficcion", "sci-fi", "scifi", "futur", "espacio", "robots", "alien"],
            "romance": ["romance", "amor", "pareja", "relaciones", "enamor"],
            "terror": ["terror", "horror", "miedo", "macab", "pesadilla"],
            "oscuro": ["oscuro", "maduro", "adulto", "crudo", "realista", "violento", "noir"],
            "accion": ["acción", "accion", "batalla", "peleas", "lucha", "aventura", "shonen"],
            "comedia": ["comedia", "humor", "gracioso", "parodia"]
        }

        # Detecta intenciones presentes
        intents = set()
        for k, kws in intent_map.items():
            if any(kw in profile for kw in kws):
                intents.add(k)

        # Aplica boosts basados en demografía (lo único "semántico" que tienes)
        if "oscuro" in intents:
            if demo in ("seinen", "josei"):
                score += 0.18
            else:
                score += 0.06  # algo, aunque sea shonen

        if "romance" in intents:
            if demo in ("josei", "shojo"):
                score += 0.16
            else:
                score += 0.05

        if "accion" in intents:
            if demo == "shonen":
                score += 0.14
            else:
                score += 0.05

        if "terror" in intents:
            score += 0.08

        if "fantasia" in intents:
            score += 0.08

        if "ciencia_ficcion" in intents:
            score += 0.08

        # Si el usuario pide sin comedia, penaliza si detecta que pide comedia
        if ("sin comedia" in profile) or ("no comedia" in profile):
            if "comedia" in intents:
                score -= 0.08

        # --- 3) Popularidad suave (desempate) usando ventas ---
        sales = float(c.Approximate_sales_in_million_s or 0.0)
        # 0..80M => 0..0.12
        score += min(max(sales, 0.0), 80.0) / 80.0 * 0.12

        # clamp
        score = max(0.0, min(score, 0.99))

        reason_bits = []
        if intents:
            reason_bits.append("encaja con " + ", ".join(sorted(intents)).replace("_", " "))
        if c.Demographic:
            reason_bits.append(f"demografía {c.Demographic}")
        if c.Publisher:
            reason_bits.append(f"editorial {c.Publisher}")

        reason = "Recomendado porque " + "; ".join(reason_bits) if reason_bits else "Recomendado por afinidad general con tu perfil."
        scored.append((score, Recommendation(manga_id=c.manga_id,title=str(c.Manga_series), score=score, reason=reason)))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [rec for _, rec in scored[:top_k]]


async def recommend(
    user_profile: str,
    candidates: List[MangaCandidate],
    top_k: int,
    history: Optional[List[Dict[str, Any]]] = None,
) -> List[Recommendation]:

    # 0) RAG primero (si está enabled)
    if RAG_ENABLED:
        try:
            rag_out = rag_recommend(
                user_profile={"text": user_profile},
                candidates=[_manga_to_rag_candidate(c) for c in candidates],
                top_k=top_k,
                history=history,

            )

            recs: List[Recommendation] = []
            for item in (rag_out or [])[:top_k]:
                # Acepta ambos formatos (por si el RAG devuelve comic_id o manga_id)
                m_id = item.get("manga_id", item.get("comic_id"))
                nombre = item.get("Manga_series", item.get("title"))
                if m_id is None and nombre is None:
                    continue

                recs.append(
                    Recommendation(
                        manga_id=int(m_id),
                        title = str(nombre),
                        score=float(item.get("score", 0.5)),
                        reason=str(item.get("reason", ""))[:240],
                    )
                )

            if recs:
                return recs

        except Exception as e:
            print("RAG failed:", repr(e))
            
        # 1) OpenAI opcional (fallback)
    if AI_PROVIDER == "openai":
        try:
            from openai import AsyncOpenAI  # type: ignore
            if not OPENAI_API_KEY:
                return _mock_recommend(user_profile, candidates, top_k)

            client = AsyncOpenAI(api_key=OPENAI_API_KEY)

            compact = [
                {
                    "manga_id": c.manga_id,
                    "series": c.Manga_series,
                    "author": c.Author_s,
                    "publisher": c.Publisher,
                    "demographic": c.Demographic,
                    "vols": c.No_of_collected_volumes,
                    "serialized": c.Serialized,
                }
                for c in candidates
            ]

            prompt = (
                "Eres un recomendador de manga. "
                "Dado un perfil de usuario y una lista de candidatos, devuelve TOP recomendaciones "
                "en JSON con: manga_id, score (0-1), reason (1 frase). "
                "No inventes mangas fuera de la lista.\n\n"
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

            import json
            arr = json.loads(content)

            recs: List[Recommendation] = []
            for item in arr[:top_k]:
                recs.append(
                    Recommendation(
                        manga_id=int(item["manga_id"]),
                        title=str(item["title"]),
                        score=float(item.get("score", 0.5)),
                        reason=str(item.get("reason", ""))[:240],
                    )
                )
            return recs

        except Exception:
            return _mock_recommend(user_profile, candidates, top_k)

    return _mock_recommend(user_profile, candidates, top_k)

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


