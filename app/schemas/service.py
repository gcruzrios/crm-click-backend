from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ServiceCreate(BaseModel):
    name: str
    description: str | None = None
    category: str | None = None
    base_price: float = 0
    billing_type: str = "one_time"
    currency: str = "USD"
    is_active: bool = True
    sort_order: int = 0


class ServiceUpdate(ServiceCreate):
    name: str | None = None


class ServiceResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    name: str
    description: str | None
    category: str | None
    base_price: float
    billing_type: str
    currency: str
    is_active: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime
