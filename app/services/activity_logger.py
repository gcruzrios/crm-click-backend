from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity import Activity
from app.utils.date_utils import utcnow


async def log_activity(
    db: AsyncSession,
    *,
    activity_type: str,
    subject: str | None = None,
    description: str | None = None,
    user_id: UUID | None = None,
    client_id: UUID | None = None,
    contact_id: UUID | None = None,
    lead_id: UUID | None = None,
    opportunity_id: UUID | None = None,
    quote_id: UUID | None = None,
) -> Activity:
    activity = Activity(
        activity_type=activity_type,
        subject=subject,
        description=description,
        user_id=user_id,
        client_id=client_id,
        contact_id=contact_id,
        lead_id=lead_id,
        opportunity_id=opportunity_id,
        quote_id=quote_id,
        activity_date=utcnow(),
    )
    db.add(activity)
    return activity
