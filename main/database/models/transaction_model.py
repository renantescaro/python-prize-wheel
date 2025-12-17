from datetime import datetime
from sqlmodel import Field, SQLModel
from sqlalchemy import func, Enum as sa_Enum
from typing import Optional
from main.helpers.enums.transaction_type import TransactionType


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id")
    account_id: int = Field(foreign_key="account.id")
    value: float
    transaction_type: TransactionType = Field(sa_column=sa_Enum(TransactionType))
    creation_time: Optional[datetime] = Field(
        default=None, sa_column_kwargs={"server_default": func.now()}
    )

    def to_json(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "account_id": self.account_id,
            "value": self.value,
            "transaction_type": (
                self.transaction_type.value if self.transaction_type else ""
            ),
            "creation_time": self.creation_time,
        }
