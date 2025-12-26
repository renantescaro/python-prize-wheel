from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from main.database.database import Database, select
from main.database.models.campaign import Campaign
from main.database.models.campaign_item import CampaignItem
from main.database.models.spin_model import Spin
from main.database.models.user_model import User
from main.schemas.campaign_item import NewCampaignItemParams
from main.services.auth.get_current_user import get_current_user

router = APIRouter(prefix="/admin/campaign-item")


@router.get("/{campaign_id}")
def campaign_items(campaign_id: int, current_user: User = Depends(get_current_user)):
    sql = select(CampaignItem).where(CampaignItem.campaign_id == campaign_id)
    campaign_items: Optional[list[CampaignItem]] = Database().get_all(sql)

    return [items.to_json() for items in campaign_items] if campaign_items else []


@router.post("/{campaign_id}")
def save_campaign_items(
    campaign_id: int,
    body: list[NewCampaignItemParams],
    current_user: User = Depends(get_current_user),
):
    _database = Database()

    for item in body:
        # novos itens
        if not item.id:
            campaign_item = CampaignItem(
                name=item.name,
                title=item.title,
                description=item.description,
                color=item.color,
                value=item.value,
                campaign_id=campaign_id,
                company_id=current_user.company_id,
            )
            _database.save(campaign_item)

        # alteração
        else:
            sql = select(CampaignItem).where(CampaignItem.id == item.id)
            changed_item: Optional[CampaignItem] = Database().get_one(sql)

            if changed_item:
                changed_item.name = item.name
                changed_item.title = item.title
                changed_item.description = item.description
                changed_item.color = item.color
                changed_item.value = item.value
                _database.save(changed_item)

    return {}


@router.delete("/{campaign_id}/{id}")
def delete_coampaign_by_id(
    campaign_id: int,
    id: int,
    current_user: User = Depends(get_current_user),
):
    _database = Database()
    sql_spin = select(Spin).where(
        Spin.campaign_item_winner_id == id,
    )
    spin_item_winner: Optional[Spin] = _database.get_one(sql_spin)
    if spin_item_winner:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This item has already had a winner",
        )

    sql = select(CampaignItem).where(
        CampaignItem.campaign_id == campaign_id,
        CampaignItem.id == id,
    )
    campaign_item: Optional[CampaignItem] = _database.get_one(sql)

    if not campaign_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    _database.delete(campaign_item)

    return {}
