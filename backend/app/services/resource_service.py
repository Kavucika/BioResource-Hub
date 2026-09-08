from sqlalchemy.orm import Session

from app.models.resource import Resource
from app.models.resource_category import ResourceCategory
from app.models.location import Location

from app.schemas.resource import (
    CreateResourceRequest,
    UpdateResourceRequest
)


def create_resource(
    db: Session,
    user_id,
    data: CreateResourceRequest
):
    # Check category exists
    category = (
        db.query(ResourceCategory)
        .filter(
            ResourceCategory.id == data.category_id,
            ResourceCategory.is_active == True
        )
        .first()
    )

    if category is None:
        raise ValueError("Category not found or inactive")

    # Check location exists
    location = (
        db.query(Location)
        .filter(Location.id == data.location_id)
        .first()
    )

    if location is None:
        raise ValueError("Location not found")

    resource = Resource(
        user_id=user_id,
        category_id=data.category_id,
        name=data.name,
        description=data.description,
        quantity=data.quantity,
        unit=data.unit,
        condition=data.condition,
        quality_description=data.quality_description,
        asking_price=data.asking_price,
        currency=data.currency,
        location_id=data.location_id,
        status="ACTIVE",
        expires_at=data.expires_at
    )

    db.add(resource)
    db.commit()
    db.refresh(resource)

    return resource


def get_all_resources(db: Session):
    return (
        db.query(Resource)
        .filter(Resource.status == "ACTIVE")
        .order_by(Resource.created_at.desc())
        .all()
    )


def get_resource(
    db: Session,
    resource_id
):
    resource = (
        db.query(Resource)
        .filter(Resource.id == resource_id)
        .first()
    )

    if resource is None:
        raise ValueError("Resource not found")

    return resource


def update_resource(
    db: Session,
    resource_id,
    user_id,
    data: UpdateResourceRequest
):
    resource = get_resource(db, resource_id)

    # Only owner can update
    if resource.user_id != user_id:
        raise PermissionError(
            "You can only update your own resource"
        )

    if data.category_id is not None:
        category = (
            db.query(ResourceCategory)
            .filter(
                ResourceCategory.id == data.category_id,
                ResourceCategory.is_active == True
            )
            .first()
        )

        if category is None:
            raise ValueError(
                "Category not found or inactive"
            )

        resource.category_id = data.category_id

    if data.location_id is not None:
        location = (
            db.query(Location)
            .filter(Location.id == data.location_id)
            .first()
        )

        if location is None:
            raise ValueError("Location not found")

        resource.location_id = data.location_id

    if data.name is not None:
        resource.name = data.name

    if data.description is not None:
        resource.description = data.description

    if data.quantity is not None:
        resource.quantity = data.quantity

    if data.unit is not None:
        resource.unit = data.unit

    if data.condition is not None:
        resource.condition = data.condition

    if data.quality_description is not None:
        resource.quality_description = (
            data.quality_description
        )

    if data.asking_price is not None:
        resource.asking_price = data.asking_price

    if data.expires_at is not None:
        resource.expires_at = data.expires_at

    db.commit()
    db.refresh(resource)

    return resource


def delete_resource(
    db: Session,
    resource_id,
    user_id
):
    resource = get_resource(db, resource_id)

    # Only owner can delete
    if resource.user_id != user_id:
        raise PermissionError(
            "You can only delete your own resource"
        )

    # Soft delete
    resource.status = "CANCELLED"

    db.commit()

    return resource