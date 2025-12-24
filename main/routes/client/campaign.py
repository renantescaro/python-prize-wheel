from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy import func
from main.database.database import Database, select
from main.database.models.campaign import Campaign
from main.database.models.client_model import Client
from main.services.auth.get_current_client import get_current_client

router = APIRouter(prefix="/campaign")


@router.get("/")
def campaign(current_client: Client = Depends(get_current_client)):
    now = func.now()
    sql = select(Campaign).where(
        Campaign.start_date <= now,
        Campaign.end_date >= now,
    )
    campaigns: Optional[list[Campaign]] = Database().get_all(sql)

    return [campaign.to_json() for campaign in campaigns] if campaigns else []
