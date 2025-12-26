from typing import Optional
from pydantic import BaseModel


class NewCampaignItemParams(BaseModel):
    id: Optional[int] = None
    name: str
    title: str
    description: str
    color: str
    value: float


class ChangeCampaignItemParams(BaseModel):
    name: str
    title: str
    description: str
    color: str
    value: float
