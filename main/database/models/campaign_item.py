from typing import Optional
from datetime import date
from sqlmodel import Field, SQLModel


class CampaignItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True)
    title: str = Field(max_length=100)
    description: str = Field(max_length=200)
    creation_date: date = Field(default_factory=date.today)
    color: str = Field(max_length=6)
    value: float
    campaign_id: Optional[int] = Field(default=None, foreign_key="campaign.id")
    company_id: Optional[int] = Field(default=None, foreign_key="company.id")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "creation_date": self.creation_date,
            "color": self.color,
            "value": self.value,
            "campaign_id": self.campaign_id,
            "company_id": self.company_id,
        }
