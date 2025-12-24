from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from main.database.database import Database, select
from main.database.models.user_model import User
from main.services.auth.password_hash import PasswordHash
from main.services.auth.get_current_user import get_current_user
from main.schemas.user import ChangeUserParams, NewUserParams

router_protected = APIRouter(prefix="/user")


@router_protected.get("/")
def user(current_user: User = Depends(get_current_user)):
    sql = select(User)
    users: Optional[list[User]] = Database().get_all(sql)
    if not users:
        return []

    return [user.to_json() for user in users]


@router_protected.get("/{id}")
def user_by_id(
    id: int,
    current_user: User = Depends(get_current_user),
):
    sql = select(User).where(User.id == id)
    user: Optional[User] = Database().get_one(sql)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user.to_json()


@router_protected.post("/")
def new_user(
    body: NewUserParams,
    current_user: User = Depends(get_current_user),
):
    _password = PasswordHash().execute(body.password)

    user = User(
        name=body.name,
        login=body.login,
        password=_password,
        company_id=current_user.company_id,
        is_active=body.is_active,
    )
    new_user: User = Database().save(user)
    return new_user.to_json()


@router_protected.put("/{id}")
def change_user(
    body: ChangeUserParams,
    id: int,
    current_user: User = Depends(get_current_user),
):
    sql = select(User).where(User.id == id)
    user: Optional[User] = Database().get_one(sql)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )

    if body.password:
        _password = PasswordHash().execute(body.password)
        user.password = _password

    user.name = body.name
    user.login = body.login
    user.company_id = current_user.company_id
    user.is_active = body.is_active
    changed_user: User = Database().save(user)

    return changed_user.to_json()


@router_protected.delete("/{id}")
def delete_user(
    id: int,
    current_user: User = Depends(get_current_user),
):
    sql = select(User).where(User.id == id)
    user: Optional[User] = Database().get_one(sql)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )

    Database().delete(user)
    return {}
