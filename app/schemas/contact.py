from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ContactCreate(BaseModel):
    client_id: UUID
    full_name: str
    position: str | None = None
    email: str | None = None
    phone: str | None = None
    whatsapp: str | None = None
    is_primary: bool = False
    notes: str | None = None


class ContactUpdate(BaseModel):
    full_name: str | None = None
    position: str | None = None
    email: str | None = None
    phone: str | None = None
    whatsapp: str | None = None
    is_primary: bool | None = None
    is_active: bool | None = None
    notes: str | None = None


class ContactClientResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    name: str


class ContactResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    client_id: UUID
    full_name: str
    position: str | None
    email: str | None
    phone: str | None
    whatsapp: str | None
    is_primary: bool
    is_active: bool
    notes: str | None
    client: ContactClientResponse | None = None
    created_at: datetime
    updated_at: datetime
