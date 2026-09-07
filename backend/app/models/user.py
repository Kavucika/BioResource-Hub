import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        unique=True,
        nullable=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(20),
        default="USER",
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )