from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.permissions import get_current_user, require_not_viewer
from app.db.session import get_db
from app.models.opportunity import Opportunity
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.opportunity import (
    OpportunityCreate,
    OpportunityLostUpdate,
    OpportunityResponse,
    OpportunityStageUpdate,
    OpportunityUpdate,
)
from app.services.activity_logger import log_activity
from app.utils.date_utils import utcnow
from app.utils.pagination import paginate

router = APIRouter(prefix="/opportunities", tags=["opportunities"])
DbDep = Annotated[AsyncSession, Depends(get_db)]

OPPORTUNITY_STAGES = [
    "new",
    "contacted",
    "meeting_scheduled",
    "diagnosis",
    "quote_sent",
    "negotiation",
    "won",
    "lost",
]


@router.get("/pipeline")
async def pipeline(db: DbDep, current_user=Depends(get_current_user)):
    q = (
        select(Opportunity)
        .options(selectinload(Opportunity.client), selectinload(Opportunity.owner_user))
        .order_by(Opportunity.updated_at.desc())
    )
    if current_user.role == "sales":
        q = q.where(Opportunity.owner_user_id == current_user.id)

    result = await db.execute(q)
    pipeline_data = {stage: [] for stage in OPPORTUNITY_STAGES}

    for opp in result.scalars().all():
        stage = opp.stage or "new"
        pipeline_data.setdefault(stage, []).append({
            "id": opp.id,
            "client_id": opp.client_id,
            "contact_id": opp.contact_id,
            "lead_id": opp.lead_id,
            "title": opp.title,
            "description": opp.description,
            "stage": stage,
            "estimated_value": float(opp.estimated_value or 0),
            "probability": opp.probability,
            "expected_close_date": opp.expected_close_date,
            "closed_at": opp.closed_at,
            "owner_user_id": opp.owner_user_id,
            "lost_reason": opp.lost_reason,
            "client": {"id": opp.client.id, "name": opp.client.name} if opp.client else None,
            "owner_user": {"id": opp.owner_user.id, "full_name": opp.owner_user.full_name} if opp.owner_user else None,
            "created_at": opp.created_at,
            "updated_at": opp.updated_at,
        })

    return pipeline_data


@router.get("", response_model=PaginatedResponse[OpportunityResponse])
async def list_opportunities(
    db: DbDep,
    current_user=Depends(get_current_user),
    stage: str | None = None,
    client_id: UUID | None = None,
    owner_user_id: UUID | None = None,
    page: int = 1,
    size: int = 20,
):
    q = select(Opportunity).options(selectinload(Opportunity.client))
    if current_user.role == "sales":
        q = q.where(Opportunity.owner_user_id == current_user.id)
    if stage:
        q = q.where(Opportunity.stage == stage)
    if client_id:
        q = q.where(Opportunity.client_id == client_id)
    if owner_user_id:
        q = q.where(Opportunity.owner_user_id == owner_user_id)
    return await paginate(db, q, Opportunity, page, size, OpportunityResponse)


@router.post("", response_model=OpportunityResponse, status_code=201)
async def create_opportunity(payload: OpportunityCreate, db: DbDep, _=Depends(require_not_viewer)):
    opp = Opportunity(**payload.model_dump())
    db.add(opp)
    await db.commit()
    await db.refresh(opp)
    return opp


@router.get("/{opportunity_id}", response_model=OpportunityResponse)
async def get_opportunity(opportunity_id: UUID, db: DbDep, _=Depends(get_current_user)):
    opp = await db.scalar(
        select(Opportunity)
        .options(selectinload(Opportunity.client))
        .where(Opportunity.id == opportunity_id)
    )
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opp


@router.put("/{opportunity_id}", response_model=OpportunityResponse)
async def update_opportunity(
    opportunity_id: UUID, payload: OpportunityUpdate, db: DbDep, _=Depends(require_not_viewer)
):
    opp = await db.get(Opportunity, opportunity_id)
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(opp, field, value)
    await db.commit()
    await db.refresh(opp)
    return opp


@router.delete("/{opportunity_id}", response_model=MessageResponse)
async def delete_opportunity(opportunity_id: UUID, db: DbDep, _=Depends(require_not_viewer)):
    opp = await db.get(Opportunity, opportunity_id)
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    await db.delete(opp)
    await db.commit()
    return {"message": "Opportunity deleted"}


@router.patch("/{opportunity_id}/stage", response_model=OpportunityResponse)
async def change_stage(
    opportunity_id: UUID, payload: OpportunityStageUpdate, db: DbDep, current_user=Depends(require_not_viewer)
):
    opp = await db.get(Opportunity, opportunity_id)
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    old_stage = opp.stage
    opp.stage = payload.stage
    await log_activity(
        db,
        activity_type="status_change",
        subject=f"Etapa cambiada: {old_stage} → {payload.stage}",
        user_id=current_user.id,
        opportunity_id=opp.id,
        client_id=opp.client_id,
    )
    await db.commit()
    await db.refresh(opp)
    return opp


@router.patch("/{opportunity_id}/won", response_model=OpportunityResponse)
async def mark_won(opportunity_id: UUID, db: DbDep, current_user=Depends(require_not_viewer)):
    opp = await db.get(Opportunity, opportunity_id)
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    opp.stage = "won"
    opp.closed_at = utcnow()
    await log_activity(db, activity_type="status_change", subject="Oportunidad ganada", user_id=current_user.id, opportunity_id=opp.id, client_id=opp.client_id)
    await db.commit()
    await db.refresh(opp)
    return opp


@router.patch("/{opportunity_id}/lost", response_model=OpportunityResponse)
async def mark_lost(
    opportunity_id: UUID, payload: OpportunityLostUpdate, db: DbDep, current_user=Depends(require_not_viewer)
):
    opp = await db.get(Opportunity, opportunity_id)
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    opp.stage = "lost"
    opp.closed_at = utcnow()
    opp.lost_reason = payload.lost_reason
    await log_activity(db, activity_type="status_change", subject="Oportunidad perdida", user_id=current_user.id, opportunity_id=opp.id, client_id=opp.client_id)
    await db.commit()
    await db.refresh(opp)
    return opp
