from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import get_current_user, require_admin_or_manager
from app.db.session import get_db
from app.models.service import Service
from app.schemas.common import MessageResponse
from app.schemas.service import ServiceCreate, ServiceResponse, ServiceUpdate

router = APIRouter(prefix="/services", tags=["services"])
DbDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("", response_model=list[ServiceResponse])
async def list_services(
    db: DbDep,
    _=Depends(get_current_user),
    category: str | None = None,
    billing_type: str | None = None,
    is_active: bool | None = None,
    search: str | None = None,
):
    q = select(Service)
    if category:
        q = q.where(Service.category == category)
    if billing_type:
        q = q.where(Service.billing_type == billing_type)
    if is_active is not None:
        q = q.where(Service.is_active == is_active)
    if search:
        q = q.where(Service.name.ilike(f"%{search}%"))
    q = q.order_by(Service.sort_order, Service.name)
    result = await db.execute(q)
    return result.scalars().all()


@router.post("", response_model=ServiceResponse, status_code=201)
async def create_service(payload: ServiceCreate, db: DbDep, _=Depends(require_admin_or_manager)):
    service = Service(**payload.model_dump())
    db.add(service)
    await db.commit()
    await db.refresh(service)
    return service


@router.get("/{service_id}", response_model=ServiceResponse)
async def get_service(service_id: UUID, db: DbDep, _=Depends(get_current_user)):
    service = await db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@router.put("/{service_id}", response_model=ServiceResponse)
async def update_service(service_id: UUID, payload: ServiceUpdate, db: DbDep, _=Depends(require_admin_or_manager)):
    service = await db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(service, field, value)
    await db.commit()
    await db.refresh(service)
    return service


@router.patch("/{service_id}/activate", response_model=ServiceResponse)
async def activate_service(service_id: UUID, db: DbDep, _=Depends(require_admin_or_manager)):
    service = await db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    service.is_active = True
    await db.commit()
    await db.refresh(service)
    return service


@router.patch("/{service_id}/deactivate", response_model=ServiceResponse)
async def deactivate_service(service_id: UUID, db: DbDep, _=Depends(require_admin_or_manager)):
    service = await db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    service.is_active = False
    await db.commit()
    await db.refresh(service)
    return service


@router.delete("/{service_id}", response_model=MessageResponse)
async def delete_service(service_id: UUID, db: DbDep, _=Depends(require_admin_or_manager)):
    service = await db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    await db.delete(service)
    await db.commit()
    return {"message": "Service deleted"}
