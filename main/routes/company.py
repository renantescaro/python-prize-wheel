from fastapi import APIRouter, Depends
from main.database.models.user_model import User
from main.services.auth.get_current_user import get_current_user

router_protected = APIRouter()


@router_protected.get("/company")
def company(current_user: User = Depends(get_current_user)):
    return {}


@router_protected.get("/company/{id}")
def company_by_id(id: int, current_user: User = Depends(get_current_user)):
    return {}


@router_protected.post("/company")
def new_company(id: int, current_user: User = Depends(get_current_user)):
    return {}


@router_protected.put("/company/{id}")
def change_company(id: int, current_user: User = Depends(get_current_user)):
    return {}


@router_protected.delete("/company/{id}")
def delete_company(id: int, current_user: User = Depends(get_current_user)):
    return {}
