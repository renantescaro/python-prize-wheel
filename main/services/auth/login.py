import bcrypt
import jwt
import uuid
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from sqlmodel import select
from typing import Optional
from main.database.database import Database
from main.database.models.client_model import Client
from main.database.models.user_model import User
from main.helpers.enums.dot_env import DotEnvEnum
from main.helpers.settings import Settings
from main.services.auth.jwt_auth import JWTAuth


class Login:
    def __init__(self, jwt_auth: JWTAuth) -> None:
        self._jwt_auth = jwt_auth

    def _get_user_by_id(self, id: int) -> Optional[User]:
        query = select(User).where(User.id == id)
        return Database().get_one(query)

    def _get_client_by_id(self, id: int) -> Optional[Client]:
        query = select(Client).where(Client.id == id)
        return Database().get_one(query)

    def _create_response(self, user_id: int, kind: str, company_id: Optional[int]):
        TOKEN_KEY = Settings.get(DotEnvEnum.TOKEN_KEY)
        TOKEN_VALIDATE = float(Settings.get(DotEnvEnum.TOKEN_VALIDATE))

        now = datetime.now(timezone.utc)
        token_payload = {
            "kind": kind,
            "exp": now + timedelta(minutes=TOKEN_VALIDATE),
            "iat": now,
            "jti": str(uuid.uuid4()).replace("-", ""),
            "sub": str(user_id),
        }
        token = jwt.encode(payload=token_payload, key=TOKEN_KEY)

        if kind == "user":
            return {
                "company_id": company_id,
                "token": token,
            }

        return {"token": token}

    def _check(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )

    def execute(self, user_or_client_id: int, secret: str, kind: str):
        user = None

        if kind == "user":
            user = self._get_user_by_id(user_or_client_id)

        if kind == "client":
            user = self._get_client_by_id(user_or_client_id)

        if user is None or not user.is_active:
            raise HTTPException(404, "user not found")

        if not self._check(secret, user.password):
            raise HTTPException(401, "wrong password")

        return self._create_response(
            user_or_client_id,
            kind,
            user.company_id if kind == "user" else None,
        )
