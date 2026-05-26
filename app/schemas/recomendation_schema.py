from pydantic import BaseModel


# PREDICT REQUEST
class PredictRequest(BaseModel):
    session_id: str


# SINGLE RECOMMENDATION
class RecommendationItem(BaseModel):
    rank: int
    career: str
    description: str
    industry: str
    avg_salary_idr: str
    confidence: float
    model_index: int


# PREDICT RESPONSE
class PredictResponse(BaseModel):
    session_id: str
    recommendations: list[RecommendationItem]
