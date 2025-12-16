from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from main.database.database import Database, select
from main.database.models.client_model import Client
from main.services.auth.jwt_auth import JWTAuth

security = HTTPBearer()


def get_current_client(
    token: HTTPAuthorizationCredentials = Depends(security),
) -> Client:
    payload = JWTAuth.decode(str(token.credentials))

    if payload is None:
        # Erro de decodificação, expiração ou token inválido
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    client_id_str = payload.get("sub")
    print("client_id_str ->", client_id_str)

    if client_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token malformado: ID de cliente ausente.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    client_id = int(client_id_str)

    sql = select(Client).where(Client.id == client_id)
    current_client = Database().get_one(sql)

    if current_client is None:
        # O token é válido, mas o cliente não existe mais no BD
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cliente do token não encontrado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return current_client
