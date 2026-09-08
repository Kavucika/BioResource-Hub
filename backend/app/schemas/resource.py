from pydantic import BaseModel, Field
from uuid import UUID
from decimal import Decimal
from datetime import datetime


class CreateResourceRequest(BaseModel):
    name: str = Field(..., min_length=2)
    description: str | None = None

    category_id: UUID

    quantity: Decimal = Field(..., gt=0)
    unit: str

    condition: str | None = None
    quality_description: str | None = None

    asking_price: Decimal | None = Field(
        default=None,
        ge=0
    )

    currency: str = "INR"

    location_id: UUID

    expires_at: datetime | None = None


class UpdateResourceRequest(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2
    )

    description: str | None = None

    category_id: UUID | None = None

    quantity: Decimal | None = Field(
        default=None,
        gt=0
    )

    unit: str | None = None

    condition: str | None = None
    quality_description: str | None = None

    asking_price: Decimal | None = Field(
        default=None,
        ge=0
    )

    location_id: UUID | None = None

    expires_at: datetime | None = None


class ResourceResponse(BaseModel):
    resource_id: UUID
    user_id: UUID

    name: str
    description: str | None

    category_id: UUID

    quantity: Decimal
    unit: str

    condition: str | None
    quality_description: str | None

    asking_price: Decimal | None
    currency: str

    location_id: UUID

    status: str

    created_at: datetime
    updated_at: datetime
    expires_at: datetime | None