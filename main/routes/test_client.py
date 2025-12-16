from fastapi import APIRouter, Depends
from main.database.models.client_model import Client
from main.services.auth.get_current_client import get_current_client

router_protected = APIRouter()


@router_protected.get("/test-client")
def test(current_user: Client = Depends(get_current_client)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "status": "Autenticação de Cliente bem-sucedida",
    }
