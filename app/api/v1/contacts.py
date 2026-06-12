from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.permissions import get_current_user, require_not_viewer
from app.db.session import get_db
from app.models.contact import Contact
from app.schemas.common import MessageResponse
from app.schemas.contact import ContactCreate, ContactResponse, ContactUpdate

router = APIRouter(prefix="/contacts", tags=["contacts"])
DbDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("", response_model=list[ContactResponse])
async def list_contacts(
    db: DbDep,
    _=Depends(get_current_user),
    client_id: UUID | None = None,
    search: str | None = None,
    is_active: bool | None = None,
):
    q = select(Contact).options(selectinload(Contact.client))
    if client_id:
        q = q.where(Contact.client_id == client_id)
    if search:
        q = q.where(Contact.full_name.ilike(f"%{search}%"))
    if is_active is not None:
        q = q.where(Contact.is_active == is_active)
    q = q.order_by(Contact.created_at.desc(), Contact.id.desc())
    result = await db.execute(q)
    return result.scalars().all()


@router.post("", response_model=ContactResponse, status_code=201)
async def create_contact(payload: ContactCreate, db: DbDep, _=Depends(require_not_viewer)):
    contact = Contact(**payload.model_dump())
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: UUID, db: DbDep, _=Depends(get_current_user)):
    contact = await db.scalar(
        select(Contact)
        .options(selectinload(Contact.client))
        .where(Contact.id == contact_id)
    )
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: UUID, payload: ContactUpdate, db: DbDep, _=Depends(require_not_viewer)):
    contact = await db.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(contact, field, value)
    await db.commit()
    await db.refresh(contact)
    return contact


@router.delete("/{contact_id}", response_model=MessageResponse)
async def delete_contact(contact_id: UUID, db: DbDep, _=Depends(require_not_viewer)):
    contact = await db.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    await db.delete(contact)
    await db.commit()
    return {"message": "Contact deleted"}


@router.patch("/{contact_id}/set-primary", response_model=ContactResponse)
async def set_primary_contact(contact_id: UUID, db: DbDep, _=Depends(require_not_viewer)):
    contact = await db.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    existing = await db.execute(
        select(Contact).where(Contact.client_id == contact.client_id, Contact.is_primary == True, Contact.id != contact_id)
    )
    for c in existing.scalars().all():
        c.is_primary = False
    contact.is_primary = True
    await db.commit()
    await db.refresh(contact)
    return contact
