from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional
from sqlalchemy import func


class Spin(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id", index=True)
    account_id: int = Field(foreign_key="account.id", index=True)
    result_value: float
    prize_details: str
    campaign_id: int = Field(foreign_key="campaign.id", index=True)
    campaign_item_winner_id: int = Field(foreign_key="campaignitem.id", index=True)
    creation_time: Optional[datetime] = Field(
        default=None, sa_column_kwargs={"server_default": func.now()}
    )

    def to_json(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "account_id": self.account_id,
            "result_value": self.result_value,
            "prize_details": self.prize_details,
        }
