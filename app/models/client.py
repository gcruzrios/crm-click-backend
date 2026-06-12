import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    client_type: Mapped[str] = mapped_column(String(30), nullable=False, default="company")
    industry: Mapped[str | None] = mapped_column(String(100), nullable=True)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    country: Mapped[str | None] = mapped_column(String(100), default="Costa Rica")
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="prospect")
    tax_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    owner_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    owner_user = relationship("User", back_populates="clients", foreign_keys=[owner_user_id])
    contacts = relationship("Contact", back_populates="client", cascade="all, delete-orphan")
    opportunities = relationship("Opportunity", back_populates="client", cascade="all, delete-orphan")
    quotes = relationship("Quote", back_populates="client")
    tasks = relationship("Task", back_populates="client")
    activities = relationship("Activity", back_populates="client")
    leads = relationship("Lead", back_populates="converted_client", foreign_keys="Lead.converted_client_id")
