from app.models.models import (
    AssessmentSession,
    CareerPath,
    Recommendation,
)
from app.utils.dependencies import (
    CurrentUser,
    DbSession,
)
from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.get("/{user_id}")
def get_user_recommendations(
    user_id: int,
    current_user: CurrentUser,
    db: DbSession,
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tidak memiliki akses",
        )

    sessions = (
        db.query(AssessmentSession)
        .filter(
            AssessmentSession.user_id == user_id,
            AssessmentSession.status == "completed",
        )
        .all()
    )

    history = []

    for session in sessions:
        recommendations = (
            db.query(Recommendation, CareerPath)
            .join(
                CareerPath,
                Recommendation.career_path_id == CareerPath.id,
            )
            .filter(Recommendation.session_id == session.id)
            .order_by(Recommendation.rank_position.asc())
            .all()
        )

        items = []

        for recommendation, career in recommendations:
            items.append(
                {
                    "rank": recommendation.rank_position,
                    "career_id": career.id,
                    "career_title": career.title,
                    "confidence": recommendation.match_score,
                    "description": career.description,
                }
            )

        history.append(
            {
                "session_id": session.id,
                "status": session.status,
                "started_at": session.started_at,
                "completed_at": session.completed_at,
                "recommendations": items,
            }
        )

    return {
        "user_id": user_id,
        "history": history,
    }
