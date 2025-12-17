from typing import Optional
from fastapi import APIRouter, Depends
from main.database.database import Database, select
from main.database.models.transaction_model import Transaction
from main.database.models.user_model import User
from main.services.auth.get_current_user import get_current_user

router_protected = APIRouter(prefix="/transaction")


@router_protected.get("/")
def transactions(current_user: User = Depends(get_current_user)):
    sql = select(Transaction)
    transactions: Optional[list[Transaction]] = Database().get_all(sql)
    if not transactions:
        return []

    return [transaction.to_json() for transaction in transactions]
