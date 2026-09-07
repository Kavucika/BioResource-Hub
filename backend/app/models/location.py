import uuid
from datetime import datetime

from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    address_line: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    village: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    district: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    state: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    country: Mapped[str] = mapped_column(
        String(100),
        default="India",
        nullable=False
    )

    pincode: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True
    )

    latitude: Mapped[float | None] = mapped_column(
        Numeric(10, 7),
        nullable=True
    )

    longitude: Mapped[float | None] = mapped_column(
        Numeric(10, 7),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )