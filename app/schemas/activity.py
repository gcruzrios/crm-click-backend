from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ActivityCreate(BaseModel):
    activity_type: str
    subject: str | None = None
    description: str | None = None
    user_id: UUID | None = None
    client_id: UUID | None = None
    contact_id: UUID | None = None
    lead_id: UUID | None = None
    opportunity_id: UUID | None = None
    quote_id: UUID | None = None
    activity_date: datetime | None = None


class ActivityUpdate(ActivityCreate):
    activity_type: str | None = None


class ActivityResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    activity_type: str
    subject: str | None
    description: str | None
    user_id: UUID | None
    client_id: UUID | None
    contact_id: UUID | None
    lead_id: UUID | None
    opportunity_id: UUID | None
    quote_id: UUID | None
    activity_date: datetime
    created_at: datetime
