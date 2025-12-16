from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from main.database.database import Database, select
from main.database.models.account_model import Account
from main.database.models.client_model import Client
from main.database.models.spin_model import Spin
from main.database.models.transaction_model import Transaction
from main.helpers.enums.transaction_type import TransactionType
from main.services.auth.get_current_client import get_current_client

router_protected = APIRouter(prefix="/prize-wheel")


@router_protected.get("/")
def index(current_client: Client = Depends(get_current_client)):
    return {}


@router_protected.get("/spin")
def spin(current_client: Client = Depends(get_current_client)):
    SPIN_PRICE = 5.0

    sql = select(Account).where(
        Account.client_id == current_client.id,
    )
    account: Optional[Account] = Database().get_one(sql)

    if not account:
        client_account = Account(
            client_id=current_client.id,
            value=0,
        )
        account = Database().save(client_account)

    if account.value < SPIN_PRICE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds",
        )

    account.value -= SPIN_PRICE

    debit_transaction = Transaction(
        client_id=current_client.id,
        account_id=account.id,
        value=-SPIN_PRICE,
        transaction_type=TransactionType.DEBIT_SPIN,
    )
    Database().save(debit_transaction)

    # lógica do giro da roleta
    result_value = 10
    prize_details = f"Ganho de R$ {result_value} no giro da roleta"

    spin = Spin(
        client_id=current_client.id,
        account_id=account.id,
        result_value=result_value,
        prize_details=prize_details,
    )
    Database().save(spin)
