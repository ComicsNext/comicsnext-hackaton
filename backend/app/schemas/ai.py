from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ----------------------------
# Manga candidate (viene de DB o de JSON si quieres)
# ----------------------------
class MangaCandidate(BaseModel):
    manga_id: int
    Manga_series: str
    Author_s: str
    Publisher: str
    Demographic: str
    No_of_collected_volumes: int
    Serialized: str
    Approximate_sales_in_million_s: float
    Average_sales_per_volume_in_million_s: float

    
    model_config = {"from_attributes": True}

# ----------------------------
# Request/Response
# ----------------------------
class RecommendRequest(BaseModel):
    user_profile: str = Field(..., description="Gustos del usuario (texto libre).")
    # candidates: List[MangaCandidate] = Field(..., min_length=1)
    top_k: int = Field(5, ge=1, le=20)
    history: Optional[List[Dict[str, Any]]] = None


class RecommendFromDbRequest(BaseModel):
    user_profile: str = Field(..., description="Gustos del usuario (texto libre).")
    top_k: int = Field(5, ge=1, le=20)

    user_id: Optional[int] = None        
    candidate_limit: int = Field(200, ge=10, le=2000)


class Recommendation(BaseModel):
    manga_id: int
    title :str
    score: float
    reason: str


class RecommendResponse(BaseModel):
    top_k: int
    recommendations: List[Recommendation]


# ----------------------------
# Summarize / Analyze
# ----------------------------
class SummarizeRequest(BaseModel):
    title: str
    synopsis: str
    max_words: int = Field(80, ge=20, le=250)


class SummarizeResponse(BaseModel):
    summary: str


class AnalyzeReviewRequest(BaseModel):
    review_text: str
    title: Optional[str] = None


class AnalyzeReviewResponse(BaseModel):
    sentiment: str
    tags: List[str] = Field(default_factory=list)
    short_reason: str