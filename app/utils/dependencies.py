from typing import Annotated

from app.core.database import get_db
from app.models.models import User
from app.utils.security import verify_access_token
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

# JWT BEARER
security = HTTPBearer()


# TYPE ALIASES
DbSession = Annotated[Session, Depends(get_db)]

BearerToken = Annotated[HTTPAuthorizationCredentials, Depends(security)]


# GET CURRENT USER
def get_current_user(
    credentials: BearerToken,
    db: DbSession,
) -> User:

    token = credentials.credentials

    try:
        payload = verify_access_token(token)

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token tidak valid"
            )

        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User tidak ditemukan"
            )

        return user

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )


# CURRENT USER TYPE
CurrentUser = Annotated[User, Depends(get_current_user)]
