from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client import Client
from app.models.contact import Contact
from app.models.lead import Lead
from app.models.opportunity import Opportunity
from app.models.quote import Quote
from app.models.task import Task


async def get_dashboard(db: AsyncSession) -> dict:
    total_leads = (await db.execute(select(func.count(Lead.id)))).scalar_one()

    leads_this_month = (
        await db.execute(
            select(func.count(Lead.id)).where(
                Lead.created_at >= func.date_trunc("month", func.now())
            )
        )
    ).scalar_one()

    total_clients = (await db.execute(select(func.count(Client.id)))).scalar_one()
    active_clients = (
        await db.execute(select(func.count(Client.id)).where(Client.status == "active"))
    ).scalar_one()
    total_contacts = (await db.execute(select(func.count(Contact.id)))).scalar_one()

    open_opps = (
        await db.execute(
            select(func.count(Opportunity.id)).where(
                Opportunity.stage.notin_(["won", "lost"])
            )
        )
    ).scalar_one()

    total_opps = (await db.execute(select(func.count(Opportunity.id)))).scalar_one()

    quoted_amount = (
        await db.execute(
            select(func.coalesce(func.sum(Quote.total), 0)).where(
                Quote.status.notin_(["rejected", "expired"])
            )
        )
    ).scalar_one()

    won_amount = (
        await db.execute(
            select(func.coalesce(func.sum(Opportunity.estimated_value), 0)).where(
                Opportunity.stage == "won"
            )
        )
    ).scalar_one()

    total_quotes = (await db.execute(select(func.count(Quote.id)))).scalar_one()

    pending_tasks = (
        await db.execute(
            select(func.count(Task.id)).where(Task.status == "pending")
        )
    ).scalar_one()

    quotes_waiting = (
        await db.execute(
            select(func.count(Quote.id)).where(Quote.status == "sent")
        )
    ).scalar_one()

    converted_leads = (
        await db.execute(
            select(func.count(Lead.id)).where(Lead.status == "converted")
        )
    ).scalar_one()

    opportunities_by_stage = dict(
        (await db.execute(select(Opportunity.stage, func.count(Opportunity.id)).group_by(Opportunity.stage))).all()
    )
    quotes_by_status = dict(
        (await db.execute(select(Quote.status, func.count(Quote.id)).group_by(Quote.status))).all()
    )
    leads_by_status = dict(
        (await db.execute(select(Lead.status, func.count(Lead.id)).group_by(Lead.status))).all()
    )
    clients_by_status = dict(
        (await db.execute(select(Client.status, func.count(Client.id)).group_by(Client.status))).all()
    )
    tasks_by_status = dict(
        (await db.execute(select(Task.status, func.count(Task.id)).group_by(Task.status))).all()
    )

    conversion_rate = round((converted_leads / total_leads) * 100, 1) if total_leads else 0.0
    avg_deal_size = round(float(won_amount) / converted_leads, 2) if converted_leads else 0.0

    kpis = {
        "total_leads": total_leads,
        "leads_this_month": leads_this_month,
        "total_clients": total_clients,
        "active_clients": active_clients,
        "total_contacts": total_contacts,
        "open_opportunities": open_opps,
        "total_opportunities": total_opps,
        "sent_quotes": quotes_waiting,
        "total_quotes": total_quotes,
        "total_quoted": float(quoted_amount),
        "total_won": float(won_amount),
        "pending_tasks": pending_tasks,
        "quotes_waiting_approval": quotes_waiting,
        "converted_leads": converted_leads,
        "conversion_rate": conversion_rate,
        "avg_deal_size": avg_deal_size,
    }

    return {
        "kpis": kpis,
        "opportunities_by_stage": opportunities_by_stage,
        "quotes_by_status": quotes_by_status,
        "leads_by_status": leads_by_status,
        "clients_by_status": clients_by_status,
        "tasks_by_status": tasks_by_status,
        **kpis,
    }
