from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from main.database.database import Database, select
from main.database.models.account_model import Account
from main.database.models.client_model import Client
from main.database.models.transaction_model import Transaction
from main.helpers.enums.transaction_type import TransactionType
from main.schemas.buy_coins import BuyCoins
from main.services.auth.get_current_client import get_current_client

router = APIRouter(prefix="/buy-coins")


@router.post("/")
def buy_coins(
    body: BuyCoins,
    current_client: Client = Depends(get_current_client),
):
    _database = Database()

    sql = select(Account).where(Account.client_id == current_client.id)
    account: Optional[Account] = _database.get_one(sql)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    transaction = Transaction(
        client_id=current_client.id,
        transaction_type=TransactionType.DEPOSIT,
        account_id=account.id,
        value=body.value,
    )
    new_transaction: Optional[Transaction] = _database.save(transaction)
    if not new_transaction:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao comprar moedas",
        )

    account.value += body.value
    account_update: Optional[Account] = _database.save(account)
    if not account_update:
        # TODO: criar verificação de transactions não creditadas
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Problemas ao adicionar moedas a sua conta.\nNosso suporte já esta ciente.\nAguarde um momento.",
        )

    return account_update.to_json()
