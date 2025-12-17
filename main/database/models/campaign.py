from typing import Optional
from datetime import date, datetime
from sqlmodel import Field, SQLModel


class Campaign(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True)
    title: str = Field(max_length=100)
    description: str = Field(max_length=200)
    creation_date: date = Field(default_factory=date.today)
    start_date: datetime
    end_date: datetime
    spin_price: float
    initial_amount: float
    current_amount: float
    company_id: Optional[int] = Field(default=None, foreign_key="company.id")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "creation_date": self.creation_date,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "spin_price": self.spin_price,
            "company_id": self.company_id,
        }
