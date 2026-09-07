import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class PricePrediction(Base):
    __tablename__ = "price_predictions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    resource_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("resources.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    estimated_min_price: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    estimated_max_price: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        default="INR",
        nullable=False
    )

    price_unit: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    model_version: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    confidence_score: Mapped[float | None] = mapped_column(
        Numeric(5, 4),
        nullable=True
    )

    predicted_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )