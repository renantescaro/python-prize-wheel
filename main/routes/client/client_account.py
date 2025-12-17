from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from main.database.database import Database, select
from main.database.models.account_model import Account
from main.database.models.client_model import Client
from main.services.auth.get_current_client import get_current_client

router = APIRouter(prefix="/account")


@router.get("/")
def account(current_client: Client = Depends(get_current_client)):
    sql = select(Account).where(
        Account.client_id == current_client.id,
    )
    account: Optional[Account] = Database().get_one(sql)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    return account.to_json()
