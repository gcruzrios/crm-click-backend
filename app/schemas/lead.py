from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class LeadCreate(BaseModel):
    full_name: str
    company_name: str | None = None
    email: str | None = None
    phone: str | None = None
    whatsapp: str | None = None
    source: str | None = None
    interest: str | None = None
    message: str | None = None
    status: str = "new"
    assigned_user_id: UUID | None = None


class LeadUpdate(LeadCreate):
    full_name: str | None = None


class LeadStatusUpdate(BaseModel):
    status: str


class LeadConvertRequest(BaseModel):
    create_client: bool = True
    create_contact: bool = True
    create_opportunity: bool = True
    opportunity_title: str | None = None
    opportunity_stage: str = "new"


class LeadConvertResponse(BaseModel):
    client_id: UUID | None = None
    contact_id: UUID | None = None
    opportunity_id: UUID | None = None


class LeadResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    full_name: str
    company_name: str | None
    email: str | None
    phone: str | None
    whatsapp: str | None
    source: str | None
    interest: str | None
    message: str | None
    status: str
    assigned_user_id: UUID | None
    converted_client_id: UUID | None
    converted_contact_id: UUID | None
    converted_at: datetime | None
    created_at: datetime
    updated_at: datetime
