from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class BuyBase(BaseModel):
    name: str
    buy_price: int

class BuyCreate(BuyBase):
    pass

class BuyUpdate(BuyBase):
    name: Optional[str] = None
    buy_price: Optional[int] = None

class Buy(BuyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class SaleBase(BaseModel):
    name: str
    sale_price: int

class SaleCreate(SaleBase):
    pass

class SaleUpdate(SaleBase):
    name: Optional[str] = None
    sale_price: Optional[int] = None

class Sale(SaleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime