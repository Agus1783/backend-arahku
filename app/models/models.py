from datetime import datetime, timezone
from typing import Literal

# from typing import List, Optional
from app.core.database import Base
from sqlalchemy import (
    DECIMAL,
    JSON,
    TIMESTAMP,
    BigInteger,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


# USERS
class User(Base):
    __tablename__: str = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )

    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    password: Mapped[str] = mapped_column(String, index=True, nullable=False)

    full_name: Mapped[str] = mapped_column(String(100), nullable=False)

    education_level: Mapped[str | None] = mapped_column(String(20))

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)

    # Relationships
    assessment_sessions: Mapped[list["AssessmentSession"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


# ASSESSMENT CATEGORIES
class AssessmentCategory(Base):
    __tablename__: str = "assessment_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    category_name: Mapped[str] = mapped_column(String(50), nullable=False)

    description: Mapped[str | None] = mapped_column(Text)

    display_order: Mapped[int | None] = mapped_column(Integer)

    input_type: Mapped[str | None] = mapped_column(String(20))

    # Relationships
    questions: Mapped[list["Question"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )


# QUESTIONS
class Question(Base):
    __tablename__: str = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("assessment_categories.id"), nullable=False
    )

    # AI INPUT MAPPING
    feature_key: Mapped[str] = mapped_column(String(50), nullable=False)

    question_text: Mapped[str] = mapped_column(Text, nullable=False)

    input_type: Mapped[Literal["slider", "binary", "text"]] = mapped_column(
        String(20), nullable=False
    )

    min_value: Mapped[int | None] = mapped_column(Integer)

    max_value: Mapped[int | None] = mapped_column(Integer)

    display_order: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    category: Mapped["AssessmentCategory"] = relationship(back_populates="questions")

    responses: Mapped[list["UserResponse"]] = relationship(
        back_populates="question", cascade="all, delete-orphan"
    )


# ASSESSMENT SESSIONS
class AssessmentSession(Base):
    __tablename__: str = "assessment_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    status: Mapped[str] = mapped_column(String(20))

    started_at: Mapped[datetime] = mapped_column(TIMESTAMP)

    completed_at: Mapped[datetime | None] = mapped_column(TIMESTAMP)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="assessment_sessions")

    responses: Mapped[list["UserResponse"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )

    recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )


# USER RESPONSES
class UserResponse(Base):
    __tablename__: str = "user_responses"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    session_id: Mapped[str] = mapped_column(
        ForeignKey("assessment_sessions.id"), nullable=False
    )

    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False)

    answer_score: Mapped[int] = mapped_column(Integer, nullable=False)

    answered_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    session: Mapped["AssessmentSession"] = relationship(back_populates="responses")

    question: Mapped["Question"] = relationship(back_populates="responses")


# CAREER PATHS
class CareerPath(Base):
    __tablename__: str = "career_paths"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # IMPORTANT FOR AI OUTPUT MAPPING
    model_index: Mapped[int] = mapped_column(Integer, nullable=False)

    title: Mapped[str] = mapped_column(String(100), nullable=False)

    description: Mapped[str | None] = mapped_column(Text)

    required_skills: Mapped[str | None] = mapped_column(Text)

    industry: Mapped[str | None] = mapped_column(String(50))

    avg_salary_idr: Mapped[str | None] = mapped_column(String(50))

    # Relationships
    recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="career_path", cascade="all, delete-orphan"
    )


# RECOMMENDATIONS
class Recommendation(Base):
    __tablename__: str = "recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    session_id: Mapped[str] = mapped_column(
        ForeignKey("assessment_sessions.id"), nullable=False
    )

    career_path_id: Mapped[int] = mapped_column(
        ForeignKey("career_paths.id"), nullable=False
    )

    rank_position: Mapped[int] = mapped_column(Integer, nullable=False)

    match_score: Mapped[float] = mapped_column(DECIMAL(5, 4), nullable=False)

    input_snapshot: Mapped[dict[str, list[int]]] = mapped_column(JSON, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    session: Mapped["AssessmentSession"] = relationship(
        back_populates="recommendations"
    )

    career_path: Mapped["CareerPath"] = relationship(back_populates="recommendations")
