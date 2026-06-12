import math
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.common import PaginatedResponse


async def paginate(
    db: AsyncSession,
    query,
    model,
    page: int,
    size: int,
    response_schema,
) -> PaginatedResponse:
    count_q = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_q)).scalar_one()
    items_q = query.offset((page - 1) * size).limit(size)
    items = (await db.execute(items_q)).scalars().all()
    pages = math.ceil(total / size) if size else 1
    return PaginatedResponse(
        items=[response_schema.model_validate(i) for i in items],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )
