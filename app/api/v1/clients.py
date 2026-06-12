from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.permissions import get_current_user, require_not_viewer
from app.db.session import get_db
from app.models.activity import Activity
from app.models.client import Client
from app.models.contact import Contact
from app.models.opportunity import Opportunity
from app.models.quote import Quote
from app.models.task import Task
from app.schemas.activity import ActivityResponse
from app.schemas.client import ClientCreate, ClientResponse, ClientUpdate
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.contact import ContactResponse
from app.schemas.opportunity import OpportunityResponse
from app.schemas.quote import QuoteResponse
from app.schemas.task import TaskResponse
from app.utils.pagination import paginate

router = APIRouter(prefix="/clients", tags=["clients"])
DbDep = Annotated[AsyncSession, Depends(get_db)]


def _apply_scope(q, current_user):
    if current_user.role == "sales":
        q = q.where(Client.owner_user_id == current_user.id)
    return q


@router.get("", response_model=PaginatedResponse[ClientResponse])
async def list_clients(
    db: DbDep,
    current_user=Depends(get_current_user),
    search: str | None = None,
    status: str | None = None,
    industry: str | None = None,
    owner_user_id: UUID | None = None,
    page: int = 1,
    size: int = 20,
):
    q = select(Client)
    q = _apply_scope(q, current_user)
    if search:
        q = q.where(Client.name.ilike(f"%{search}%"))
    if status:
        q = q.where(Client.status == status)
    if industry:
        q = q.where(Client.industry == industry)
    if owner_user_id:
        q = q.where(Client.owner_user_id == owner_user_id)
    q = q.order_by(Client.created_at.desc(), Client.id.desc())
    return await paginate(db, q, Client, page, size, ClientResponse)


@router.post("", response_model=ClientResponse, status_code=201)
async def create_client(
    payload: ClientCreate,
    db: DbDep,
    current_user=Depends(require_not_viewer),
):
    client = Client(**payload.model_dump())
    db.add(client)
    await db.commit()
    await db.refresh(client)
    return client


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(client_id: UUID, db: DbDep, current_user=Depends(get_current_user)):
    client = await db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: UUID,
    payload: ClientUpdate,
    db: DbDep,
    _=Depends(require_not_viewer),
):
    client = await db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(client, field, value)
    await db.commit()
    await db.refresh(client)
    return client


@router.delete("/{client_id}", response_model=MessageResponse)
async def delete_client(client_id: UUID, db: DbDep, _=Depends(require_not_viewer)):
    client = await db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    await db.delete(client)
    await db.commit()
    return {"message": "Client deleted"}


@router.get("/{client_id}/contacts", response_model=list[ContactResponse])
async def client_contacts(client_id: UUID, db: DbDep, _=Depends(get_current_user)):
    result = await db.execute(select(Contact).where(Contact.client_id == client_id))
    return result.scalars().all()


@router.get("/{client_id}/opportunities", response_model=list[OpportunityResponse])
async def client_opportunities(client_id: UUID, db: DbDep, _=Depends(get_current_user)):
    result = await db.execute(
        select(Opportunity)
        .options(selectinload(Opportunity.client))
        .where(Opportunity.client_id == client_id)
    )
    return result.scalars().all()


@router.get("/{client_id}/quotes", response_model=list[QuoteResponse])
async def client_quotes(client_id: UUID, db: DbDep, _=Depends(get_current_user)):
    result = await db.execute(
        select(Quote)
        .options(selectinload(Quote.client), selectinload(Quote.items))
        .where(Quote.client_id == client_id)
    )
    return result.scalars().all()


@router.get("/{client_id}/tasks", response_model=list[TaskResponse])
async def client_tasks(client_id: UUID, db: DbDep, _=Depends(get_current_user)):
    result = await db.execute(select(Task).where(Task.client_id == client_id))
    return result.scalars().all()


@router.get("/{client_id}/activities", response_model=list[ActivityResponse])
async def client_activities(client_id: UUID, db: DbDep, _=Depends(get_current_user)):
    result = await db.execute(
        select(Activity).where(Activity.client_id == client_id).order_by(Activity.activity_date.desc())
    )
    return result.scalars().all()
