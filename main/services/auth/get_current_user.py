from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from main.database.database import Database, select
from main.database.models.user_model import User
from main.services.auth.jwt_auth import JWTAuth

security = HTTPBearer()


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    payload = JWTAuth.decode(str(token.credentials))

    if payload is None:
        # Erro de decodificação, expiração ou token inválido
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token do usuário inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id_str = payload.get("sub")

    if user_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token do usuário malformado: ID de usuário ausente.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = int(user_id_str)

    sql = select(User).where(User.id == user_id)
    current_user = Database().get_one(sql)

    if current_user is None:
        # O token é válido, mas o usuário não existe mais no BD
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário do token não encontrado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return current_user
