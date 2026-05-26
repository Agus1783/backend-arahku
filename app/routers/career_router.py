from app.models.models import CareerPath
from app.utils.dependencies import DbSession
from fastapi import APIRouter

router = APIRouter(
    prefix="/careers",
    tags=["Careers"],
)


@router.get("/")
def get_careers(
    db: DbSession,
):

    careers = db.query(CareerPath).order_by(CareerPath.title.asc()).all()

    results = []

    for career in careers:
        results.append(
            {
                "id": career.id,
                "model_index": career.model_index,
                "title": career.title,
                "description": career.description,
                "required_skills": career.required_skills,
                "industry": career.industry,
                "avg_salary_idr": career.avg_salary_idr,
            }
        )

    return {
        "total": len(results),
        "careers": results,
    }
