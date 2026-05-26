# from app.core.database import get_db
from app.models.models import AssessmentCategory
from app.schemas.question_schema import (
    QuestionCategoryResponse,
    QuestionResponse,
    QuestionsListResponse,
)
from app.utils.dependencies import DbSession
from fastapi import APIRouter

# from sqlalchemy.orm import Session

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get("/", response_model=QuestionsListResponse)
def get_questions(db: DbSession):

    categories = (
        db.query(AssessmentCategory).order_by(AssessmentCategory.display_order).all()
    )

    result = []

    for category in categories:
        questions = sorted(category.questions, key=lambda q: q.display_order or 0)

        question_items = [
            QuestionResponse(
                id=question.id,
                feature_key=question.feature_key,
                question_text=question.question_text,
                input_type=question.input_type,
                min_value=question.min_value,
                max_value=question.max_value,
                display_order=question.display_order,
            )
            for question in questions
        ]

        result.append(
            QuestionCategoryResponse(
                id=category.id,
                category_name=category.category_name,
                description=category.description,
                questions=question_items,
            )
        )

    return QuestionsListResponse(categories=result)
