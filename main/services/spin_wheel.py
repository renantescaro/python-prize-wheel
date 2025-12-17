import random
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from main.database.database import Database, select
from main.database.models.account_model import Account
from main.database.models.campaign import Campaign
from main.database.models.campaign_item import CampaignItem
from main.database.models.client_model import Client
from main.database.models.spin_model import Spin
from main.database.models.transaction_model import Transaction
from main.helpers.enums.transaction_type import TransactionType


class SpinWheel:
    def __init__(
        self,
        client_id: int,
        campaign_id: int,
    ) -> None:
        self._client_id = client_id
        self._campaign_id = campaign_id

    def _get_account(self) -> Account:
        sql = select(Account).where(
            Account.client_id == self._client_id,
        )
        account: Optional[Account] = Database().get_one(sql)

        if not account:
            client_account = Account(
                client_id=self._client_id,
                value=0,
            )
            return Database().save(client_account)

        return account

    def _create_spin_transaction(
        self,
        account_id: int,
        spin_price: float,
    ):
        debit_transaction = Transaction(
            client_id=self._client_id,
            account_id=account_id,
            value=-spin_price,
            transaction_type=TransactionType.DEBIT_SPIN,
        )
        Database().save(debit_transaction)

    def _draw_lots(self, campaign_items: list[CampaignItem]) -> CampaignItem:
        DIFFICULTY_FACTOR = 2.0
        inverse_weights = []

        for item in campaign_items:
            value = item.value

            if value <= 0:
                weight = 1000.0
            else:
                weight = 1.0 / (value**DIFFICULTY_FACTOR)

            inverse_weights.append(weight)

        item_winner = random.choices(
            population=campaign_items, weights=inverse_weights, k=1
        )

        return item_winner[0]

    def _spin_wheel(self, account_id: int) -> Spin:
        sql_items = select(CampaignItem).where(
            CampaignItem.campaign_id == self._campaign_id
        )
        campaign_item: list[CampaignItem] = Database().get_all(sql_items)

        item_winner: CampaignItem = self._draw_lots(campaign_item)

        spin = Spin(
            client_id=self._client_id,
            account_id=account_id,
            result_value=item_winner.value,
            prize_details=item_winner.description,
            campaign_id=self._campaign_id,
            campaign_item_winner_id=item_winner.id,
        )
        return Database().save(spin)

    def execute(self):
        sql = select(Campaign).where(Campaign.id == self._campaign_id)
        campaign: Campaign = Database().get_one(sql)

        account = self._get_account()

        if account.value < campaign.spin_price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient funds",
            )

        self._create_spin_transaction(account.id, campaign.spin_price)

        # TODO: criar transaction
        account.value -= campaign.spin_price
        campaign.current_amount += campaign.spin_price

        spin = self._spin_wheel(account.id)

        # TODO: criar transaction
        account.value += spin.result_value
        campaign.current_amount -= spin.result_value

        Database().save(account)
        Database().save(campaign)

        return spin.to_json()
