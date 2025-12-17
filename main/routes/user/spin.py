from typing import Optional
from fastapi import APIRouter, Depends
from main.database.database import Database, select
from main.database.models.spin_model import Spin
from main.database.models.user_model import User
from main.services.auth.get_current_user import get_current_user

router_protected = APIRouter(prefix="/spin")


@router_protected.get("/")
def spins(current_user: User = Depends(get_current_user)):
    sql = select(Spin)
    spins: Optional[list[Spin]] = Database().get_all(sql)
    if not spins:
        return []

    return [spin.to_json() for spin in spins]
