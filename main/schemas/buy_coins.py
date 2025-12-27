from pydantic import BaseModel


class BuyCoins(BaseModel):
    value: float
