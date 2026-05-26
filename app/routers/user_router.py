# from app.models.models import User
# from app.utils.dependencies import get_current_user
from app.utils.dependencies import CurrentUser
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def get_my_profile(current_user: CurrentUser):

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
    }
