from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.permissions import get_current_user, require_not_viewer
from app.db.session import get_db
from app.models.quote import Quote
from app.models.quote_item import QuoteItem
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.quote import (
    QuoteCreate,
    QuoteItemCreate,
    QuoteItemResponse,
    QuoteItemUpdate,
    QuoteResponse,
    QuoteUpdate,
)
from app.services.activity_logger import log_activity
from app.services.quote_calculator import calculate_quote, compute_line_total
from app.utils.date_utils import utcnow
from app.utils.pagination import paginate

router = APIRouter(prefix="/quotes", tags=["quotes"])
DbDep = Annotated[AsyncSession, Depends(get_db)]


async def _generate_quote_number(db: AsyncSession) -> str:
    from sqlalchemy import func
    year = datetime.now().year
    count = (await db.execute(select(func.count(Quote.id)))).scalar_one()
    return f"COT-{year}-{count + 1:04d}"


async def _recalculate(db: AsyncSession, quote: Quote) -> None:
    items_result = await db.execute(select(QuoteItem).where(QuoteItem.quote_id == quote.id))
    items = items_result.scalars().all()
    for item in items:
        item.line_total = compute_line_total(item.quantity, item.unit_price)
    subtotal, tax_amt, total = calculate_quote(items, quote.discount_amount, quote.tax_rate)
    quote.subtotal = subtotal
    quote.tax_amount = tax_amt
    quote.total = total


@router.get("", response_model=PaginatedResponse[QuoteResponse])
async def list_quotes(
    db: DbDep,
    _=Depends(get_current_user),
    status: str | None = None,
    client_id: UUID | None = None,
    opportunity_id: UUID | None = None,
    page: int = 1,
    size: int = 20,
):
    q = select(Quote).options(selectinload(Quote.client), selectinload(Quote.items))
    if status:
        q = q.where(Quote.status == status)
    if client_id:
        q = q.where(Quote.client_id == client_id)
    if opportunity_id:
        q = q.where(Quote.opportunity_id == opportunity_id)
    q = q.order_by(Quote.quote_number.desc(), Quote.created_at.desc())
    return await paginate(db, q, Quote, page, size, QuoteResponse)


@router.post("", response_model=QuoteResponse, status_code=201)
async def create_quote(payload: QuoteCreate, db: DbDep, current_user=Depends(require_not_viewer)):
    items_data = payload.items
    quote_data = payload.model_dump(exclude={"items"})
    quote_data["quote_number"] = await _generate_quote_number(db)
    quote_data["created_by_user_id"] = current_user.id
    quote = Quote(**quote_data)
    db.add(quote)
    await db.flush()

    for item_data in items_data:
        item = QuoteItem(
            quote_id=quote.id,
            **item_data.model_dump(),
            line_total=compute_line_total(item_data.quantity, item_data.unit_price),
        )
        db.add(item)

    await db.flush()
    await _recalculate(db, quote)
    await db.commit()
    await db.refresh(quote)
    return quote


@router.get("/{quote_id}", response_model=QuoteResponse)
async def get_quote(quote_id: UUID, db: DbDep, _=Depends(get_current_user)):
    quote = await db.scalar(
        select(Quote)
        .options(selectinload(Quote.client), selectinload(Quote.items))
        .where(Quote.id == quote_id)
    )
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote


@router.put("/{quote_id}", response_model=QuoteResponse)
async def update_quote(quote_id: UUID, payload: QuoteUpdate, db: DbDep, _=Depends(require_not_viewer)):
    quote = await db.get(Quote, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(quote, field, value)
    await _recalculate(db, quote)
    await db.commit()
    await db.refresh(quote)
    return quote


@router.delete("/{quote_id}", response_model=MessageResponse)
async def delete_quote(quote_id: UUID, db: DbDep, _=Depends(require_not_viewer)):
    quote = await db.get(Quote, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    await db.delete(quote)
    await db.commit()
    return {"message": "Quote deleted"}


@router.post("/{quote_id}/items", response_model=QuoteItemResponse, status_code=201)
async def add_item(quote_id: UUID, payload: QuoteItemCreate, db: DbDep, _=Depends(require_not_viewer)):
    quote = await db.get(Quote, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    item = QuoteItem(
        quote_id=quote_id,
        **payload.model_dump(),
        line_total=compute_line_total(payload.quantity, payload.unit_price),
    )
    db.add(item)
    await db.flush()
    await _recalculate(db, quote)
    await db.commit()
    await db.refresh(item)
    return item


@router.put("/{quote_id}/items/{item_id}", response_model=QuoteItemResponse)
async def update_item(quote_id: UUID, item_id: UUID, payload: QuoteItemUpdate, db: DbDep, _=Depends(require_not_viewer)):
    item = await db.get(QuoteItem, item_id)
    if not item or item.quote_id != quote_id:
        raise HTTPException(status_code=404, detail="Item not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(item, field, value)
    item.line_total = compute_line_total(item.quantity, item.unit_price)
    quote = await db.get(Quote, quote_id)
    await _recalculate(db, quote)
    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/{quote_id}/items/{item_id}", response_model=MessageResponse)
async def delete_item(quote_id: UUID, item_id: UUID, db: DbDep, _=Depends(require_not_viewer)):
    item = await db.get(QuoteItem, item_id)
    if not item or item.quote_id != quote_id:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(item)
    quote = await db.get(Quote, quote_id)
    await db.flush()
    await _recalculate(db, quote)
    await db.commit()
    return {"message": "Item deleted"}


@router.patch("/{quote_id}/send", response_model=QuoteResponse)
async def send_quote(quote_id: UUID, db: DbDep, current_user=Depends(require_not_viewer)):
    quote = await db.get(Quote, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    quote.status = "sent"
    quote.sent_at = utcnow()
    await log_activity(db, activity_type="quote_sent", subject=f"Cotización enviada: {quote.quote_number}", user_id=current_user.id, client_id=quote.client_id, quote_id=quote.id)
    await db.commit()
    await db.refresh(quote)
    return quote


@router.patch("/{quote_id}/approve", response_model=QuoteResponse)
async def approve_quote(quote_id: UUID, db: DbDep, current_user=Depends(require_not_viewer)):
    quote = await db.get(Quote, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    quote.status = "approved"
    quote.approved_at = utcnow()
    await log_activity(db, activity_type="status_change", subject=f"Cotización aprobada: {quote.quote_number}", user_id=current_user.id, client_id=quote.client_id, quote_id=quote.id)
    await db.commit()
    await db.refresh(quote)
    return quote


@router.patch("/{quote_id}/reject", response_model=QuoteResponse)
async def reject_quote(quote_id: UUID, db: DbDep, current_user=Depends(require_not_viewer)):
    quote = await db.get(Quote, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    quote.status = "rejected"
    await db.commit()
    await db.refresh(quote)
    return quote


@router.patch("/{quote_id}/expire", response_model=QuoteResponse)
async def expire_quote(quote_id: UUID, db: DbDep, _=Depends(require_not_viewer)):
    quote = await db.get(Quote, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    quote.status = "expired"
    await db.commit()
    await db.refresh(quote)
    return quote


@router.post("/{quote_id}/duplicate", response_model=QuoteResponse, status_code=201)
async def duplicate_quote(quote_id: UUID, db: DbDep, current_user=Depends(require_not_viewer)):
    quote = await db.get(Quote, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    new_quote = Quote(
        quote_number=await _generate_quote_number(db),
        client_id=quote.client_id,
        contact_id=quote.contact_id,
        opportunity_id=quote.opportunity_id,
        currency=quote.currency,
        tax_rate=quote.tax_rate,
        discount_amount=quote.discount_amount,
        valid_until=quote.valid_until,
        terms=quote.terms,
        notes=quote.notes,
        created_by_user_id=current_user.id,
        status="draft",
    )
    db.add(new_quote)
    await db.flush()

    items_result = await db.execute(select(QuoteItem).where(QuoteItem.quote_id == quote_id))
    for item in items_result.scalars().all():
        db.add(QuoteItem(
            quote_id=new_quote.id,
            service_id=item.service_id,
            description=item.description,
            quantity=item.quantity,
            unit_price=item.unit_price,
            billing_type=item.billing_type,
            line_total=item.line_total,
            sort_order=item.sort_order,
        ))

    await db.flush()
    await _recalculate(db, new_quote)
    await db.commit()
    await db.refresh(new_quote)
    return new_quote
