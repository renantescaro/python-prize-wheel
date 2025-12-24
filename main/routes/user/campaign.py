from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from main.database.database import Database, select
from main.database.models.campaign import Campaign
from main.database.models.user_model import User
from main.schemas.campaign import ChangeCampaignParams, NewCampaignParams
from main.services.auth.get_current_user import get_current_user

router = APIRouter(prefix="/admin/campaign")


@router.get("/")
def campaign(current_user: User = Depends(get_current_user)):
    sql = select(Campaign)
    campaigns: Optional[list[Campaign]] = Database().get_all(sql)

    return [campaign.to_json() for campaign in campaigns] if campaigns else []


@router.get("/{id}")
def get_coampaign_by_id(
    id: int,
    current_user: User = Depends(get_current_user),
):
    sql = select(Campaign).where(Campaign.id == id)
    campaign: Optional[Campaign] = Database().get_one(sql)

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found",
        )

    return campaign.to_json()


@router.post("/")
def new_campaign(
    body: NewCampaignParams,
    current_user: User = Depends(get_current_user),
):
    campaign = Campaign(
        name=body.name,
        title=body.title,
        description=body.description,
        start_date=body.start_date,
        end_date=body.end_date,
        spin_price=body.spin_price,
        company_id=current_user.company_id,
        initial_amount=0,
        current_amount=0,
    )

    new_campaign: Campaign = Database().save(campaign)
    return new_campaign.to_json()


@router.put("/{id}")
def change_coampaign(
    id: int,
    body: ChangeCampaignParams,
    current_user: User = Depends(get_current_user),
):
    sql = select(Campaign).where(Campaign.id == id)
    campaign: Optional[Campaign] = Database().get_one(sql)

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found",
        )

    campaign.name = body.name
    campaign.title = body.title
    campaign.description = body.description
    campaign.start_date = body.start_date
    campaign.end_date = body.end_date
    campaign.spin_price = body.spin_price
    campaign.company_id = current_user.company_id
    campaign.initial_amount = 0
    campaign.current_amount = 0

    updated_campaign: Campaign = Database().save(campaign)

    return updated_campaign.to_json()


@router.delete("/{id}")
def delete_coampaign_by_id(
    id: int,
    current_user: User = Depends(get_current_user),
):
    sql = select(Campaign).where(Campaign.id == id)
    campaign: Optional[Campaign] = Database().get_one(sql)

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found",
        )

    Database().delete(campaign)

    return {}
