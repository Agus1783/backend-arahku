import uuid
from datetime import datetime, timezone

# from app.core.database import get_db
from app.models.models import AssessmentSession
from app.schemas.session_schema import CreateSessionResponse
from app.utils.dependencies import CurrentUser, DbSession
from fastapi import APIRouter, status

# from sqlalchemy.orm import Session

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post(
    "/", response_model=CreateSessionResponse, status_code=status.HTTP_201_CREATED
)
def create_session(current_user: CurrentUser, db: DbSession):

    session_id = str(uuid.uuid4())

    new_session = AssessmentSession(
        id=session_id,
        user_id=current_user.id,
        status="in_progress",
        started_at=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return CreateSessionResponse(
        session_id=new_session.id,
        status=new_session.status,
        started_at=new_session.started_at,
    )
