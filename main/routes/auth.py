from fastapi import APIRouter
from main.services.auth.jwt_auth import JWTAuth
from main.services.auth.login import Login
from main.schemas.authenticate import AuthenticateSchema, AuthenticateResponseSchema

router = APIRouter()


@router.post("/auth")
def auth(request: AuthenticateSchema):
    return Login(JWTAuth()).execute(
        request.client_id,
        request.client_secret,
        request.kind,
    )
