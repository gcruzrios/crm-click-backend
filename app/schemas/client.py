from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class ClientCreate(BaseModel):
    name: str
    client_type: str = "company"
    industry: str | None = None
    website: str | None = None
    phone: str | None = None
    email: str | None = None
    country: str | None = "Costa Rica"
    city: str | None = None
    address: str | None = None
    status: str = "prospect"
    tax_id: str | None = None
    owner_user_id: UUID | None = None
    notes: str | None = None


class ClientUpdate(ClientCreate):
    name: str | None = None


class ClientResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    name: str
    client_type: str
    industry: str | None
    website: str | None
    phone: str | None
    email: str | None
    country: str | None
    city: str | None
    address: str | None
    status: str
    tax_id: str | None
    owner_user_id: UUID | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
