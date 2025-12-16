import jwt
from datetime import datetime, timezone
from main.helpers.enums.dot_env import DotEnvEnum
from main.helpers.settings import Settings


class JWTAuth:
    TOKEN_KEY = Settings.get(DotEnvEnum.TOKEN_KEY)
    TOKEN_VALIDATE = float(Settings.get(DotEnvEnum.TOKEN_VALIDATE))
    ALGORITHM = "HS256"

    @classmethod
    def encode(
        cls,
        payload: dict,
    ) -> str:
        to_encode = payload.copy()

        expire = datetime.now(timezone.utc) + cls.TOKEN_VALIDATE
        to_encode.update({"exp": expire.timestamp()})

        encoded_jwt = jwt.encode(
            to_encode,
            cls.TOKEN_KEY,
            algorithm=cls.ALGORITHM,
        )
        return encoded_jwt

    @classmethod
    def decode(cls, token: str) -> dict | None:
        try:
            payload = jwt.decode(
                token,
                cls.TOKEN_KEY,
                algorithms=[cls.ALGORITHM],
            )
            return payload

        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError as e:
            return None

    @classmethod
    def check(cls, token: str) -> bool:
        payload = cls.decode(token)
        return payload is not None
