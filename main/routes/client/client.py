from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from main.database.database import Database, select
from main.database.models.account_model import Account
from main.database.models.client_model import Client
from main.database.models.user_model import User
from main.schemas.client import NewClientParams, ChangeClientParams
from main.services.auth.get_current_client import get_current_client
from main.services.auth.password_hash import PasswordHash

router = APIRouter(prefix="/client")


@router.post("/")
def new_client(body: NewClientParams):
    _password = PasswordHash().execute(body.password)

    client = Client(
        name=body.name,
        login=body.login,
        document=body.document,
        birthday=body.birthday,
        password=_password,
        creation_date=date.today(),
        is_active=True,
    )
    new_client: Client = Database().save(client)

    client_account = Account(
        client_id=new_client.id,
        value=0,
    )
    Database().save(client_account)

    return new_client.to_json()


@router.get("/")
def client(current_client: Client = Depends(get_current_client)):
    sql = select(Client).where(
        Client.id == current_client.id,
        Client.is_active == True,
    )
    client: Optional[Client] = Database().get_one(sql)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )

    return client.to_json()


@router.put("/")
def change_client(
    body: ChangeClientParams,
    current_client: Client = Depends(get_current_client),
):
    sql = select(Client).where(
        Client.id == current_client.id,
        Client.is_active == True,
    )
    client: Optional[Client] = Database().get_one(sql)

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )

    _password = PasswordHash().execute(body.password)

    client.name = body.name
    client.login = body.login
    client.password = _password
    client.birthday = body.birthday
    client.is_active = body.is_active
    changed_client: Client = Database().save(client)

    return changed_client.to_json()


@router.delete("/")
def delete_client(
    current_client: Client = Depends(get_current_client),
):
    sql = select(Client).where(
        Client.id == current_client.id,
        Client.is_active == True,
    )
    client: Optional[Client] = Database().get_one(sql)

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )

    client.is_active = False
    Database().save(client)
