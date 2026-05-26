from datetime import datetime, timezone

# from app.core.database import get_db
from app.models.models import User
from app.schemas.auth_schema import (
    LoginRequest,
    LoginResponse,
    LoginUserResponse,
    RegisterRequest,
    RegisterResponse,
)

# from sqlalchemy.orm import Session
from app.utils.dependencies import DbSession
from app.utils.security import create_access_token, hash_password, verify_password
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/auth", tags=["Authentication"])


# REGISTER
@router.post(
    "/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED
)
def register(payload: RegisterRequest, db: DbSession):

    # Check username
    existing_username = db.query(User).filter(User.username == payload.username).first()

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username sudah terdaftar"
        )

    # Check email
    existing_email = db.query(User).filter(User.email == payload.email).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email sudah terdaftar"
        )

    # Create user
    new_user = User(
        username=payload.username,
        email=payload.email,
        password=hash_password(payload.password),
        full_name=payload.full_name,
        education_level=payload.education_level,
        created_at=datetime.now(timezone.utc),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# LOGIN
@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: DbSession):

    user = db.query(User).filter(User.username == payload.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
        )

    valid_password = verify_password(payload.password, user.password)

    if not valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
        )

    access_token = create_access_token({"user_id": user.id})

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=LoginUserResponse(
            id=user.id, username=user.username, full_name=user.full_name
        ),
    )
