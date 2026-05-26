from datetime import datetime

from pydantic import BaseModel


class CreateSessionResponse(BaseModel):
    session_id: str
    status: str
    started_at: datetime
