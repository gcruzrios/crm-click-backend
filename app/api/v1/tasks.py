from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import get_current_user, require_not_viewer
from app.db.session import get_db
from app.models.task import Task
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.activity_logger import log_activity
from app.utils.date_utils import utcnow
from app.utils.pagination import paginate

router = APIRouter(prefix="/tasks", tags=["tasks"])
DbDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("", response_model=PaginatedResponse[TaskResponse])
async def list_tasks(
    db: DbDep,
    current_user=Depends(get_current_user),
    status: str | None = None,
    priority: str | None = None,
    assigned_user_id: UUID | None = None,
    client_id: UUID | None = None,
    opportunity_id: UUID | None = None,
    page: int = 1,
    size: int = 20,
):
    q = select(Task)
    if current_user.role == "sales":
        q = q.where(Task.assigned_user_id == current_user.id)
    if status:
        q = q.where(Task.status == status)
    if priority:
        q = q.where(Task.priority == priority)
    if assigned_user_id:
        q = q.where(Task.assigned_user_id == assigned_user_id)
    if client_id:
        q = q.where(Task.client_id == client_id)
    if opportunity_id:
        q = q.where(Task.opportunity_id == opportunity_id)
    return await paginate(db, q, Task, page, size, TaskResponse)


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(payload: TaskCreate, db: DbDep, _=Depends(require_not_viewer)):
    task = Task(**payload.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: UUID, db: DbDep, _=Depends(get_current_user)):
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: UUID, payload: TaskUpdate, db: DbDep, _=Depends(require_not_viewer)):
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(task, field, value)
    await db.commit()
    await db.refresh(task)
    return task


@router.delete("/{task_id}", response_model=MessageResponse)
async def delete_task(task_id: UUID, db: DbDep, _=Depends(require_not_viewer)):
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task)
    await db.commit()
    return {"message": "Task deleted"}


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(task_id: UUID, db: DbDep, current_user=Depends(require_not_viewer)):
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = "completed"
    task.completed_at = utcnow()
    await log_activity(
        db,
        activity_type="task_completed",
        subject=f"Tarea completada: {task.title}",
        user_id=current_user.id,
        client_id=task.client_id,
        opportunity_id=task.opportunity_id,
    )
    await db.commit()
    await db.refresh(task)
    return task


@router.patch("/{task_id}/cancel", response_model=TaskResponse)
async def cancel_task(task_id: UUID, db: DbDep, _=Depends(require_not_viewer)):
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = "cancelled"
    await db.commit()
    await db.refresh(task)
    return task
