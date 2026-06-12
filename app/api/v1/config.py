from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import require_admin
from app.db.session import get_db
from app.models.system_config import SystemConfig

router = APIRouter(prefix="/config", tags=["config"])
DbDep = Annotated[AsyncSession, Depends(get_db)]


class ConfigUpdate(BaseModel):
    value: str


@router.get("")
async def list_config(db: DbDep, _=Depends(require_admin)):
    result = await db.execute(select(SystemConfig))
    return [{"key": c.key, "value": c.value, "description": c.description} for c in result.scalars().all()]


@router.patch("/{key}")
async def update_config(key: str, payload: ConfigUpdate, db: DbDep, _=Depends(require_admin)):
    config = await db.get(SystemConfig, key)
    if not config:
        raise HTTPException(status_code=404, detail="Config key not found")
    config.value = payload.value
    await db.commit()
    await db.refresh(config)
    return {"key": config.key, "value": config.value}
