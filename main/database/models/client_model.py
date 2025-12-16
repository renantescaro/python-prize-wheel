from datetime import date
from sqlmodel import Field, SQLModel
from typing import Optional


class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    password: str = Field(max_length=500)
    document: str = Field(max_length=20)
    birthday: date
    creation_date: Optional[date] = Field(default_factory=date.today)
    is_active: bool

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "document": self.document,
            "birthday": self.birthday,
            "creation_date": self.creation_date,
            "is_active": self.is_active,
        }
