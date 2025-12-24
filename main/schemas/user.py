from typing import Optional
from pydantic import BaseModel


class NewCompanyParams(BaseModel):
    name: str
    tenant: str


class ChangeCompanyParams(BaseModel):
    name: str
    tenant: str


class NewUserParams(BaseModel):
    name: str
    login: str
    password: str
    company_id: int
    is_active: bool


class ChangeUserParams(BaseModel):
    name: str
    login: str
    company_id: int
    is_active: bool
    password: Optional[str] = None
