from datetime import date
from sqlmodel import Field, SQLModel
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    login: str = Field(max_length=100, unique=True)
    password: str = Field(max_length=500)
    creation_date: Optional[date] = Field(default_factory=date.today)
    company_id: Optional[int] = Field(default=None, foreign_key="company.id")
    is_active: bool

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "login": self.login,
            "creation_date": self.creation_date,
            "company_id": self.company_id,
            "is_active": self.is_active,
        }
