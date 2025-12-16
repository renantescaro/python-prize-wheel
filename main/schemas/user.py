from pydantic import BaseModel


class NewCompanyParams(BaseModel):
    name: str
    tenant: str


class ChangeCompanyParams(BaseModel):
    name: str
    tenant: str


class NewUserParams(BaseModel):
    name: str
    password: str
    company_id: int
    is_active: bool


class ChangeUserParams(BaseModel):
    name: str
    password: str
    company_id: int
    is_active: bool
