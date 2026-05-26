from typing import List

from pydantic import BaseModel


class PredictRequest(BaseModel):
    session_id: str


class RecommendationItem(BaseModel):
    rank: int
    career_id: int
    career_name: str
    confidence: float
    description: str | None = None


class PredictResponse(BaseModel):
    recommendations: List[RecommendationItem]
