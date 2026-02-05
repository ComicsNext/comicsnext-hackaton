from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ComicCandidate(BaseModel):
    comic_id: int
    title: str
    synopsis: Optional[str] = None
    genres: List[str] = Field(default_factory=list)
    author: Optional[str] = None
    publisher: Optional[str] = None
    year: Optional[int] = None
    extra: Dict[str, Any] = Field(default_factory=dict)  # por si luego metemos más info


class RecommendRequest(BaseModel):
    user_profile: str = Field(..., description="Gustos del usuario (texto libre).")
    candidates: List[ComicCandidate] = Field(..., min_length=1)
    top_k: int = Field(5, ge=1, le=20)
    history: Optional[List[Dict[str, Any]]] = None


class Recommendation(BaseModel):
    comic_id: int
    score: float
    reason: str


class RecommendResponse(BaseModel):
    top_k: int
    recommendations: List[Recommendation]


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
    sentiment: str  # "positive" | "neutral" | "negative"
    tags: List[str] = Field(default_factory=list)
    short_reason: str