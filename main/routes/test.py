from fastapi import APIRouter, Depends

from main.database.models.user_model import User
from main.services.auth.get_current_user import get_current_user

router_protected = APIRouter()


@router_protected.get("/test")
def test(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "status": "Autenticação bem-sucedida",
    }
