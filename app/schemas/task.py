from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: str = "pending"
    priority: str = "medium"
    due_date: datetime | None = None
    assigned_user_id: UUID | None = None
    client_id: UUID | None = None
    contact_id: UUID | None = None
    lead_id: UUID | None = None
    opportunity_id: UUID | None = None


class TaskUpdate(TaskCreate):
    title: str | None = None


class TaskResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    title: str
    description: str | None
    status: str
    priority: str
    due_date: datetime | None
    completed_at: datetime | None
    assigned_user_id: UUID | None
    client_id: UUID | None
    contact_id: UUID | None
    lead_id: UUID | None
    opportunity_id: UUID | None
    created_at: datetime
    updated_at: datetime
