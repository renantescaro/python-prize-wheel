from fastapi import APIRouter, Depends
from main.database.models.user_model import User
from main.services.auth.get_current_user import get_current_user

router_protected = APIRouter()


@router_protected.get("/user")
def user(current_user: User = Depends(get_current_user)):
    return {}


@router_protected.get("/user/{id}")
def user_by_id(id: int, current_user: User = Depends(get_current_user)):
    return {}


@router_protected.post("/user")
def new_user(id: int, current_user: User = Depends(get_current_user)):
    return {}


@router_protected.put("/user/{id}")
def change_user(id: int, current_user: User = Depends(get_current_user)):
    return {}


@router_protected.delete("/user/{id}")
def delete_user(id: int, current_user: User = Depends(get_current_user)):
    return {}
