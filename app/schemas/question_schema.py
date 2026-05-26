from typing import Literal

from pydantic import BaseModel


# QUESTION ITEM
class QuestionResponse(BaseModel):
    id: int
    feature_key: str
    question_text: str

    input_type: Literal["slider", "binary", "text"]

    min_value: int | None = None
    max_value: int | None = None

    display_order: int


# CATEGORY ITEM
class QuestionCategoryResponse(BaseModel):
    id: int
    category_name: str
    description: str | None = None

    questions: list[QuestionResponse]


# FINAL RESPONSE
class QuestionsListResponse(BaseModel):
    categories: list[QuestionCategoryResponse]
