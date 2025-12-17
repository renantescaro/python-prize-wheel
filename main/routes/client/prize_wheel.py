from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from main.database.database import Database, select
from main.database.models import campaign_item
from main.database.models.campaign import Campaign
from main.database.models.campaign_item import CampaignItem
from main.database.models.client_model import Client
from main.services.auth.get_current_client import get_current_client
from main.services.spin_wheel import SpinWheel

router_protected = APIRouter(prefix="/prize-wheel")


@router_protected.get("/{campaign}")
def index(campaign: str, current_client: Client = Depends(get_current_client)):
    sql = select(Campaign).where(Campaign.name == campaign)
    _campaign: Optional[Campaign] = Database().get_one(sql)

    sql_items = select(CampaignItem).where(CampaignItem.campaign_id == _campaign.id)
    _campaign_item: Optional[list[CampaignItem]] = Database().get_all(sql_items)

    if not _campaign or not _campaign_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
        )

    return {
        "campaign": _campaign.to_json(),
        "items": [item.to_json() for item in _campaign_item],
    }


@router_protected.get("/spin/{campaign}")
def spin(campaign: str, current_client: Client = Depends(get_current_client)):
    sql = select(Campaign).where(Campaign.name == campaign)
    _campaign: Optional[Campaign] = Database().get_one(sql)

    sql_items = select(CampaignItem).where(CampaignItem.campaign_id == _campaign.id)
    _campaign_item: Optional[list[CampaignItem]] = Database().get_all(sql_items)

    if not _campaign or not _campaign_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
        )

    return SpinWheel(current_client.id, _campaign.id).execute()
