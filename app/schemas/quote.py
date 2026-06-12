from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class QuoteItemCreate(BaseModel):
    service_id: UUID | None = None
    description: str
    quantity: float = 1
    unit_price: float = 0
    billing_type: str = "one_time"
    sort_order: int = 0


class QuoteItemUpdate(QuoteItemCreate):
    description: str | None = None


class QuoteItemResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    quote_id: UUID
    service_id: UUID | None
    description: str
    quantity: float
    unit_price: float
    billing_type: str
    line_total: float
    sort_order: int


class QuoteClientResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    name: str


class QuoteCreate(BaseModel):
    client_id: UUID
    contact_id: UUID | None = None
    opportunity_id: UUID | None = None
    currency: str = "USD"
    tax_rate: float = 0
    discount_amount: float = 0
    valid_until: date | None = None
    terms: str | None = None
    notes: str | None = None
    items: list[QuoteItemCreate] = []


class QuoteUpdate(BaseModel):
    contact_id: UUID | None = None
    opportunity_id: UUID | None = None
    currency: str | None = None
    tax_rate: float | None = None
    discount_amount: float | None = None
    valid_until: date | None = None
    terms: str | None = None
    notes: str | None = None


class QuoteResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    quote_number: str
    client_id: UUID
    contact_id: UUID | None
    opportunity_id: UUID | None
    status: str
    currency: str
    subtotal: float
    tax_rate: float
    tax_amount: float
    discount_amount: float
    total: float
    valid_until: date | None
    sent_at: datetime | None
    approved_at: datetime | None
    terms: str | None
    notes: str | None
    created_by_user_id: UUID | None
    client: QuoteClientResponse | None = None
    items: list[QuoteItemResponse] = []
    created_at: datetime
    updated_at: datetime
