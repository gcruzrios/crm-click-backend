from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import get_current_user, require_not_viewer
from app.db.session import get_db
from app.models.lead import Lead
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.lead import (
    LeadConvertRequest,
    LeadConvertResponse,
    LeadCreate,
    LeadResponse,
    LeadStatusUpdate,
    LeadUpdate,
)
from app.services.lead_converter import convert_lead
from app.utils.pagination import paginate

router = APIRouter(prefix="/leads", tags=["leads"])
DbDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("", response_model=PaginatedResponse[LeadResponse])
async def list_leads(
    db: DbDep,
    current_user=Depends(get_current_user),
    status: str | None = None,
    source: str | None = None,
    assigned_user_id: UUID | None = None,
    search: str | None = None,
    page: int = 1,
    size: int = 20,
):
    q = select(Lead)
    if current_user.role == "sales":
        q = q.where(Lead.assigned_user_id == current_user.id)
    if status:
        q = q.where(Lead.status == status)
    if source:
        q = q.where(Lead.source == source)
    if assigned_user_id:
        q = q.where(Lead.assigned_user_id == assigned_user_id)
    if search:
        q = q.where(Lead.full_name.ilike(f"%{search}%") | Lead.company_name.ilike(f"%{search}%"))
    q = q.order_by(Lead.created_at.desc(), Lead.id.desc())
    return await paginate(db, q, Lead, page, size, LeadResponse)


@router.post("", response_model=LeadResponse, status_code=201)
async def create_lead(payload: LeadCreate, db: DbDep, _=Depends(require_not_viewer)):
    lead = Lead(**payload.model_dump())
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return lead


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(lead_id: UUID, db: DbDep, _=Depends(get_current_user)):
    lead = await db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.put("/{lead_id}", response_model=LeadResponse)
async def update_lead(lead_id: UUID, payload: LeadUpdate, db: DbDep, _=Depends(require_not_viewer)):
    lead = await db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(lead, field, value)
    await db.commit()
    await db.refresh(lead)
    return lead


@router.delete("/{lead_id}", response_model=MessageResponse)
async def delete_lead(lead_id: UUID, db: DbDep, _=Depends(require_not_viewer)):
    lead = await db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    await db.delete(lead)
    await db.commit()
    return {"message": "Lead deleted"}


@router.patch("/{lead_id}/status", response_model=LeadResponse)
async def update_lead_status(lead_id: UUID, payload: LeadStatusUpdate, db: DbDep, _=Depends(require_not_viewer)):
    lead = await db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead.status = payload.status
    await db.commit()
    await db.refresh(lead)
    return lead


@router.post("/{lead_id}/convert", response_model=LeadConvertResponse)
async def convert(lead_id: UUID, payload: LeadConvertRequest, db: DbDep, current_user=Depends(require_not_viewer)):
    lead = await db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    result = await convert_lead(db, lead, payload, current_user.id)
    await db.commit()
    return result
