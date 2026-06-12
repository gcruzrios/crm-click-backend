import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(String(30), nullable=False, default="sales")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    clients = relationship("Client", back_populates="owner_user", foreign_keys="Client.owner_user_id")
    leads = relationship("Lead", back_populates="assigned_user", foreign_keys="Lead.assigned_user_id")
    opportunities = relationship("Opportunity", back_populates="owner_user", foreign_keys="Opportunity.owner_user_id")
    quotes = relationship("Quote", back_populates="created_by_user", foreign_keys="Quote.created_by_user_id")
    tasks = relationship("Task", back_populates="assigned_user", foreign_keys="Task.assigned_user_id")
    activities = relationship("Activity", back_populates="user", foreign_keys="Activity.user_id")
