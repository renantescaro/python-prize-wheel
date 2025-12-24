from datetime import datetime
from pydantic import BaseModel


class NewCampaignParams(BaseModel):
    name: str
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    spin_price: float


class ChangeCampaignParams(BaseModel):
    name: str
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    spin_price: float
