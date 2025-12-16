from typing import Optional
from datetime import date
from sqlmodel import Field, SQLModel


class Company(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    tenant: str = Field(max_length=50)
    creation_date: date = Field(default_factory=date.today)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "tenant": self.tenant,
            "creation_date": self.creation_date,
        }
