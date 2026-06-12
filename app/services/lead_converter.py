from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client import Client
from app.models.contact import Contact
from app.models.lead import Lead
from app.models.opportunity import Opportunity
from app.utils.date_utils import utcnow
from app.schemas.lead import LeadConvertRequest, LeadConvertResponse
from app.services.activity_logger import log_activity


async def convert_lead(
    db: AsyncSession,
    lead: Lead,
    payload: LeadConvertRequest,
    current_user_id: UUID,
) -> LeadConvertResponse:
    if lead.status == "converted":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lead is already converted")

    client_id: UUID | None = None
    contact_id: UUID | None = None
    opportunity_id: UUID | None = None

    if payload.create_client:
        client = Client(
            name=lead.company_name or lead.full_name,
            client_type="company" if lead.company_name else "individual",
            email=lead.email,
            phone=lead.phone,
            status="prospect",
            owner_user_id=current_user_id,
        )
        db.add(client)
        await db.flush()
        client_id = client.id

    if payload.create_contact and client_id:
        contact = Contact(
            client_id=client_id,
            full_name=lead.full_name,
            email=lead.email,
            phone=lead.phone,
            whatsapp=lead.whatsapp,
            is_primary=True,
        )
        db.add(contact)
        await db.flush()
        contact_id = contact.id

    if payload.create_opportunity and client_id:
        opp = Opportunity(
            client_id=client_id,
            contact_id=contact_id,
            lead_id=lead.id,
            title=payload.opportunity_title or f"Oportunidad de {lead.full_name}",
            stage=payload.opportunity_stage,
            owner_user_id=current_user_id,
        )
        db.add(opp)
        await db.flush()
        opportunity_id = opp.id

    lead.status = "converted"
    lead.converted_at = utcnow()
    lead.converted_client_id = client_id
    lead.converted_contact_id = contact_id

    await log_activity(
        db,
        activity_type="status_change",
        subject=f"Lead convertido: {lead.full_name}",
        user_id=current_user_id,
        lead_id=lead.id,
        client_id=client_id,
        opportunity_id=opportunity_id,
    )

    return LeadConvertResponse(
        client_id=client_id,
        contact_id=contact_id,
        opportunity_id=opportunity_id,
    )
