from fastapi import APIRouter, Depends
from main.database.models.user_model import User
from main.services.auth.get_current_user import get_current_user

router = APIRouter()


@router.post("/client")
def new_client(id: int):
    return {}


@router.get("/client")
def client(current_user: User = Depends(get_current_user)):
    return {}


@router.get("/client/{id}")
def client_by_id(id: int, current_user: User = Depends(get_current_user)):
    return {}


@router.put("/client/{id}")
def change_client(id: int, current_user: User = Depends(get_current_user)):
    return {}


@router.delete("/client/{id}")
def delete_client(id: int, current_user: User = Depends(get_current_user)):
    return {}
