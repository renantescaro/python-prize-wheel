from datetime import date
from pydantic import BaseModel


class NewClientParams(BaseModel):
    name: str
    login: str
    password: str
    document: str
    birthday: date


class ChangeClientParams(BaseModel):
    name: str
    login: str
    password: str
    document: str
    birthday: date
    is_active: bool
