from pydantic import BaseModel


class AuthenticateSchema(BaseModel):
    client_login: str
    client_secret: str
    kind: str


class AuthenticateResponseSchema(BaseModel):
    access_token: str
