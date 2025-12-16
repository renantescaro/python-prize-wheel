import bcrypt
import jwt
import uuid
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from sqlmodel import select
from typing import Optional
from main.database.database import Database
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

    def _create_response(self, user_id: int, company_id: Optional[int]):
        TOKEN_KEY = Settings.get(DotEnvEnum.TOKEN_KEY)
        TOKEN_VALIDATE = float(Settings.get(DotEnvEnum.TOKEN_VALIDATE))

        now = datetime.now(timezone.utc)
        token_payload = {
            "exp": now + timedelta(minutes=TOKEN_VALIDATE),
            "iat": now,
            "jti": str(uuid.uuid4()).replace("-", ""),
            "sub": str(user_id),
        }
        token = jwt.encode(payload=token_payload, key=TOKEN_KEY)

        return {
            "company_id": company_id,
            "token": token,
        }

    def _check(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )

    def execute(self, user_id: int, user_secret: str):
        user = self._get_user_by_id(user_id)

        if user is None or not user.is_active:
            raise HTTPException(404, "user not found")

        if not self._check(user_secret, user.password):
            raise HTTPException(401, "wrong password")

        return self._create_response(user_id, user.company_id)
