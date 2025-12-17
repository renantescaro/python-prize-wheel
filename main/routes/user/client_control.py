from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from main.database.database import Database, select
from main.database.models.client_model import Client
from main.database.models.user_model import User
from main.schemas.client import ChangeClientParams
from main.services.auth.get_current_user import get_current_user
from main.services.auth.password_hash import PasswordHash

router = APIRouter(prefix="/client-control")


@router.get("/")
def client(current_user: User = Depends(get_current_user)):
    sql = select(Client)
    clients: Optional[list[Client]] = Database().get_all(sql)
    if not clients:
        return []

    return [client.to_json() for client in clients]


@router.get("/{id}")
def client_by_id(
    id: int,
    current_user: User = Depends(get_current_user),
):
    sql = select(Client).where(Client.id == id)
    client: Optional[Client] = Database().get_one(sql)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )

    return client.to_json()


@router.put("/{id}")
def change_client(
    body: ChangeClientParams,
    id: int,
    current_user: User = Depends(get_current_user),
):
    sql = select(Client).where(Client.id == id)
    client: Optional[Client] = Database().get_one(sql)

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )

    _password = PasswordHash().execute(body.password)

    client.name = body.name
    client.password = _password
    client.birthday = body.birthday
    client.is_active = body.is_active
    changed_client: Client = Database().save(client)

    return changed_client.to_json()


@router.delete("/{id}")
def delete_client(
    id: int,
    current_user: User = Depends(get_current_user),
):
    sql = select(Client).where(Client.id == id)
    client: Optional[Client] = Database().get_one(sql)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )

    Database().delete(client)
