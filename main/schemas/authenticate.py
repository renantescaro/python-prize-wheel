from pydantic import BaseModel


class AuthenticateSchema(BaseModel):
    client_id: int
    client_secret: str


class AuthenticateResponseSchema(BaseModel):
    access_token: str
