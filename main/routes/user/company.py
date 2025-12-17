from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from main.database.database import Database, select
from main.database.models.company_model import Company
from main.database.models.user_model import User
from main.services.auth.get_current_user import get_current_user
from main.schemas.user import ChangeCompanyParams, NewCompanyParams

router_protected = APIRouter(prefix="/company")


@router_protected.get("/")
def company(current_user: User = Depends(get_current_user)):
    sql = select(Company)
    companies: Optional[list[Company]] = Database().get_all(sql)
    if not companies:
        return []

    return [company.to_json() for company in companies]


@router_protected.get("/{id}")
def company_by_id(id: int, current_user: User = Depends(get_current_user)):
    sql = select(Company).where(Company.id == id)
    company: Optional[Company] = Database().get_one(sql)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    return company.to_json()


@router_protected.post("/")
def new_company(
    body: NewCompanyParams,
    current_user: User = Depends(get_current_user),
):
    company = Company(
        name=body.name,
        tenant=body.tenant,
    )
    new_company: Company = Database().save(company)
    return new_company.to_json()


@router_protected.put("/{id}")
def change_company(
    id: int,
    body: ChangeCompanyParams,
    current_user: User = Depends(get_current_user),
):
    sql = select(Company).where(Company.id == id)
    company: Optional[Company] = Database().get_one(sql)

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    company.name = body.name
    company.tenant = body.tenant
    changed_company: Company = Database().save(company)

    return changed_company.to_json()


@router_protected.delete("/{id}")
def delete_company(
    id: int,
    current_user: User = Depends(get_current_user),
):
    sql = select(Company).where(Company.id == id)
    company: Optional[Company] = Database().get_one(sql)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    Database().delete(company)

    return {}
