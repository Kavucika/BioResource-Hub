import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ResourceRequest(Base):
    __tablename__ = "resource_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("resource_categories.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    resource_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    quantity: Mapped[float] = mapped_column(
        Numeric(12, 3),
        nullable=False
    )

    unit: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    purpose: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    location_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("locations.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="OPEN",
        nullable=False,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )