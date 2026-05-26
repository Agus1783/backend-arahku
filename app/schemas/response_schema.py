from pydantic import BaseModel, Field, field_validator


# SINGLE ANSWER
class AnswerItem(BaseModel):
    question_id: int
    answer_score: int


# SUBMIT RESPONSES
class SubmitResponsesRequest(BaseModel):
    session_id: str

    answers: list[AnswerItem] = Field(min_length=17, max_length=17)

    @field_validator("answers")
    @classmethod
    def validate_exact_answers(cls, value: list[AnswerItem]) -> list[AnswerItem]:

        if len(value) != 17:
            raise ValueError("Harus ada tepat 17 jawaban")

        return value


# RESPONSE
class SubmitResponsesResponse(BaseModel):
    session_id: str
    answers_saved: int
    status: str
