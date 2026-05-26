from datetime import datetime, timezone

# from app.core.database import get_db
from app.models.models import AssessmentSession, UserResponse
from app.schemas.response_schema import SubmitResponsesRequest, SubmitResponsesResponse
from app.utils.dependencies import CurrentUser, DbSession
from fastapi import APIRouter, HTTPException, status

# from sqlalchemy.orm import Session

router = APIRouter(prefix="/responses", tags=["Responses"])


@router.post("/", response_model=SubmitResponsesResponse)
def submit_responses(
    payload: SubmitResponsesRequest, current_user: CurrentUser, db: DbSession
):

    # CHECK SESSION
    session = (
        db.query(AssessmentSession)
        .filter(
            AssessmentSession.id == payload.session_id,
            AssessmentSession.user_id == current_user.id,
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session tidak ditemukan"
        )

    # CHECK STATUS
    if session.status == "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Session sudah selesai"
        )

    # SAVE RESPONSES
    responses = [
        UserResponse(
            session_id=payload.session_id,
            question_id=answer.question_id,
            answer_score=answer.answer_score,
            answered_at=datetime.now(timezone.utc),
        )
        for answer in payload.answers
    ]

    db.bulk_save_objects(responses)

    # UPDATE SESSION
    session.status = "completed"

    session.completed_at = datetime.now(timezone.utc)

    db.commit()

    return SubmitResponsesResponse(
        session_id=payload.session_id,
        answers_saved=len(payload.answers),
        status="completed",
    )
