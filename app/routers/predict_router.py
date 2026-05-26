from datetime import datetime, timezone

import httpx
from app.core.config import settings
from app.models.models import (
    AssessmentSession,
    CareerPath,
    Question,
    Recommendation,
    UserResponse,
)
from app.schemas.predict_schema import (
    PredictRequest,
    PredictResponse,
    RecommendationItem,
)
from app.utils.dependencies import (
    CurrentUser,
    DbSession,
)
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.engine import Row

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"],
)

ACADEMIC_FEATURES = [
    "math_score",
    "history_score",
    "physics_score",
    "chemistry_score",
    "biology_score",
    "english_score",
    "geography_score",
]

SKILL_FEATURES = [
    "skill_accounting",
    "skill_communication",
    "skill_counseling",
    "skill_data_analysis",
    "skill_financial_analysis",
    "skill_machine_learning",
    "skill_marketing",
    "skill_ms_office",
    "skill_python",
    "skill_sql",
]


@router.post(
    "/",
    response_model=PredictResponse,
)
async def predict_career(
    payload: PredictRequest,
    current_user: CurrentUser,
    db: DbSession,
):

    session = (
        db.query(AssessmentSession)
        .filter(
            AssessmentSession.id == payload.session_id,
            AssessmentSession.user_id == current_user.id,
        )
        .first()
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session tidak ditemukan",
        )

    if session.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment belum selesai",
        )

    existing_recommendations = (
        db.query(Recommendation)
        .filter(Recommendation.session_id == payload.session_id)
        .first()
    )

    if existing_recommendations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prediction sudah pernah dilakukan",
        )

    responses: list[Row[tuple[UserResponse, Question]]] = (
        db.query(UserResponse, Question)
        .join(
            Question,
            UserResponse.question_id == Question.id,
        )
        .filter(UserResponse.session_id == payload.session_id)
        .all()
    )

    if len(responses) != 17:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Jumlah jawaban tidak valid",
        )

    # print(prediction)

    # career = (
    #     db.query(CareerPath)
    #     .filter(CareerPath.model_index == prediction["model_index"])
    #     .first()
    # )

    # print(career)

    feature_map: dict[str, int] = {}

    for response, question in responses:
        feature_map[question.feature_key] = response.answer_score

    required_features = ACADEMIC_FEATURES + SKILL_FEATURES

    missing_features = [
        feature for feature in required_features if feature not in feature_map
    ]

    if missing_features:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Feature tidak lengkap: {missing_features}",
        )

    academic_array = [float(feature_map[feature]) for feature in ACADEMIC_FEATURES]

    skill_array = [int(feature_map[feature]) for feature in SKILL_FEATURES]

    model_payload = {
        "akademik": academic_array,
        "skill": skill_array,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.MODEL_API_URL}/predict",
                json=model_payload,
                timeout=30.0,
            )

        _ = response.raise_for_status()

        result = response.json()
        print(result)

    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model API tidak dapat diakses",
        )

    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Model API error",
        )

    predictions = result.get("top3")

    if not predictions:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Response AI model tidak valid",
        )

    snapshot = {
        "akademik": academic_array,
        "skill": skill_array,
    }

    recommendation_items: list[RecommendationItem] = []

    for rank, prediction in enumerate(
        predictions,
        start=1,
    ):
        model_index = int(prediction.get("model_index", -1))
        confidence = float(prediction.get("confidence", 0))

        career = (
            db.query(CareerPath).filter(CareerPath.model_index == model_index).first()
        )

        if career is None:
            raise HTTPException(
                status_code=404,
                detail=f"Career dengan model_index {prediction['model_index']} tidak ditemukan",
            )

        recommendation = Recommendation(
            session_id=payload.session_id,
            career_path_id=career.id,
            rank_position=rank,
            match_score=confidence,
            input_snapshot=snapshot,
            created_at=datetime.now(timezone.utc),
        )

        db.add(recommendation)

        recommendation_items.append(
            RecommendationItem(
                rank=rank,
                career_id=career.id,
                career_name=career.title,
                confidence=confidence,
                description=career.description,
            )
        )

    db.commit()

    return PredictResponse(recommendations=recommendation_items)
