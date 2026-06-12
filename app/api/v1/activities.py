from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import get_current_user, require_not_viewer
from app.db.session import get_db
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityUpdate
from app.schemas.common import MessageResponse

router = APIRouter(prefix="/activities", tags=["activities"])
DbDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("", response_model=list[ActivityResponse])
async def list_activities(
    db: DbDep,
    _=Depends(get_current_user),
    client_id: UUID | None = None,
    lead_id: UUID | None = None,
    opportunity_id: UUID | None = None,
    quote_id: UUID | None = None,
    activity_type: str | None = None,
    user_id: UUID | None = None,
):
    q = select(Activity).order_by(Activity.activity_date.desc())
    if client_id:
        q = q.where(Activity.client_id == client_id)
    if lead_id:
        q = q.where(Activity.lead_id == lead_id)
    if opportunity_id:
        q = q.where(Activity.opportunity_id == opportunity_id)
    if quote_id:
        q = q.where(Activity.quote_id == quote_id)
    if activity_type:
        q = q.where(Activity.activity_type == activity_type)
    if user_id:
        q = q.where(Activity.user_id == user_id)
    result = await db.execute(q)
    return result.scalars().all()


@router.post("", response_model=ActivityResponse, status_code=201)
async def create_activity(payload: ActivityCreate, db: DbDep, _=Depends(require_not_viewer)):
    activity = Activity(**payload.model_dump(exclude_none=True))
    db.add(activity)
    await db.commit()
    await db.refresh(activity)
    return activity


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(activity_id: UUID, db: DbDep, _=Depends(get_current_user)):
    activity = await db.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.put("/{activity_id}", response_model=ActivityResponse)
async def update_activity(activity_id: UUID, payload: ActivityUpdate, db: DbDep, _=Depends(require_not_viewer)):
    activity = await db.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(activity, field, value)
    await db.commit()
    await db.refresh(activity)
    return activity


@router.delete("/{activity_id}", response_model=MessageResponse)
async def delete_activity(activity_id: UUID, db: DbDep, _=Depends(require_not_viewer)):
    activity = await db.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    await db.delete(activity)
    await db.commit()
    return {"message": "Activity deleted"}
