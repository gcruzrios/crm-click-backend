from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import get_current_user, require_admin_or_manager
from app.db.session import get_db
from app.models.client import Client
from app.models.lead import Lead
from app.models.opportunity import Opportunity
from app.models.quote import Quote
from app.models.task import Task
from app.services.report_service import get_dashboard

router = APIRouter(prefix="/reports", tags=["reports"])
DbDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("/dashboard")
async def dashboard(db: DbDep, _=Depends(get_current_user)):
    return await get_dashboard(db)


@router.get("/leads-by-source")
async def leads_by_source(db: DbDep, _=Depends(require_admin_or_manager)):
    result = await db.execute(
        select(Lead.source, func.count(Lead.id)).group_by(Lead.source)
    )
    return [{"source": r[0] or "unknown", "count": r[1]} for r in result.all()]


@router.get("/opportunities-by-stage")
async def opportunities_by_stage(db: DbDep, _=Depends(require_admin_or_manager)):
    result = await db.execute(
        select(Opportunity.stage, func.count(Opportunity.id), func.sum(Opportunity.estimated_value))
        .group_by(Opportunity.stage)
    )
    return [{"stage": r[0], "count": r[1], "total_value": float(r[2] or 0)} for r in result.all()]


@router.get("/quotes-by-status")
async def quotes_by_status(db: DbDep, _=Depends(require_admin_or_manager)):
    result = await db.execute(
        select(Quote.status, func.count(Quote.id), func.sum(Quote.total)).group_by(Quote.status)
    )
    return [{"status": r[0], "count": r[1], "total": float(r[2] or 0)} for r in result.all()]


@router.get("/sales-forecast")
async def sales_forecast(db: DbDep, year: int | None = None, month: int | None = None, _=Depends(require_admin_or_manager)):
    q = select(
        func.sum(Opportunity.estimated_value * Opportunity.probability / 100)
    ).where(Opportunity.stage.notin_(["won", "lost"]))
    result = await db.execute(q)
    forecast = float(result.scalar_one() or 0)
    return {"forecast": round(forecast, 2)}


@router.get("/tasks-summary")
async def tasks_summary(db: DbDep, _=Depends(get_current_user)):
    result = await db.execute(
        select(Task.status, func.count(Task.id)).group_by(Task.status)
    )
    return [{"status": r[0], "count": r[1]} for r in result.all()]


@router.get("/top-clients")
async def top_clients(db: DbDep, _=Depends(require_admin_or_manager)):
    result = await db.execute(
        select(Client.id, Client.name, func.sum(Quote.total).label("total_quoted"))
        .join(Quote, Quote.client_id == Client.id)
        .where(Quote.status.notin_(["rejected", "expired"]))
        .group_by(Client.id, Client.name)
        .order_by(func.sum(Quote.total).desc())
        .limit(10)
    )
    return [{"client_id": str(r[0]), "name": r[1], "total_quoted": float(r[2] or 0)} for r in result.all()]
