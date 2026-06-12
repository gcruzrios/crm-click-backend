from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class OpportunityCreate(BaseModel):
    client_id: UUID
    contact_id: UUID | None = None
    lead_id: UUID | None = None
    title: str
    description: str | None = None
    stage: str = "new"
    estimated_value: float = 0
    probability: int = 0
    expected_close_date: date | None = None
    owner_user_id: UUID | None = None
    lost_reason: str | None = None


class OpportunityUpdate(OpportunityCreate):
    client_id: UUID | None = None
    title: str | None = None


class OpportunityStageUpdate(BaseModel):
    stage: str


class OpportunityLostUpdate(BaseModel):
    lost_reason: str | None = None


class OpportunityClientResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    name: str


class OpportunityResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    client_id: UUID
    contact_id: UUID | None
    lead_id: UUID | None
    title: str
    description: str | None
    stage: str
    estimated_value: float
    probability: int
    expected_close_date: date | None
    closed_at: datetime | None
    owner_user_id: UUID | None
    lost_reason: str | None
    client: OpportunityClientResponse | None = None
    created_at: datetime
    updated_at: datetime
