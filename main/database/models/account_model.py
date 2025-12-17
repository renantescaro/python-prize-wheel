from sqlmodel import Field, SQLModel
from typing import Optional


class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id", unique=True)
    value: float = Field(default=0)

    def to_json(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "value": self.value,
        }
