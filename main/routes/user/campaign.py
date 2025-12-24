from typing import Optional
from fastapi import APIRouter, Depends
from main.database.database import Database, select
from main.database.models.campaign import Campaign
from main.database.models.user_model import User
from main.services.auth.get_current_user import get_current_user

router = APIRouter(prefix="/admin/campaign")


@router.get("/")
def adm_campaign(current_user: User = Depends(get_current_user)):
    sql = select(Campaign)
    campaigns: Optional[list[Campaign]] = Database().get_all(sql)

    return [campaign.to_json() for campaign in campaigns] if campaigns else []
