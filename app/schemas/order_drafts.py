import datetime
from uuid import UUID
from typing import List, Optional

from pydantic import BaseModel, Field

from app.utils.custom_types import created_at, closed_at

class CreateOrderItemRequest(BaseModel):
    product_id: UUID 
    quantity: int = Field(ge=0, default=1)
    price: int = Field(ge=0)


class CreateOrderDraftRequest(BaseModel):
    full_name: str = Field(max_length=50)
    phone: str = Field(max_length=50)
    location: str = Field(max_length=255)
    telegram_id: Optional[int] = Field(default=None)

    delivery_date: datetime.date
    slot_from: datetime.time
    slot_to: datetime.time
    
    items: List[CreateOrderItemRequest]
