from sqlalchemy.orm import Session

from app.models.resource_category import ResourceCategory
from app.schemas.category import (
    CreateCategoryRequest,
    UpdateCategoryRequest
)


def create_category(
    db: Session,
    data: CreateCategoryRequest
):
    existing_category = (
        db.query(ResourceCategory)
        .filter(ResourceCategory.name == data.name)
        .first()
    )

    if existing_category:
        raise ValueError("Category already exists")

    category = ResourceCategory(
        name=data.name,
        description=data.description,
        parent_category_id=data.parent_category_id
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def get_all_categories(db: Session):
    return (
        db.query(ResourceCategory)
        .filter(ResourceCategory.is_active == True)
        .order_by(ResourceCategory.name)
        .all()
    )


def get_category(
    db: Session,
    category_id: str
):
    category = (
        db.query(ResourceCategory)
        .filter(ResourceCategory.id == category_id)
        .first()
    )

    if category is None:
        raise ValueError("Category not found")

    return category


def update_category(
    db: Session,
    category_id: str,
    data: UpdateCategoryRequest
):
    category = get_category(db, category_id)

    if data.name is not None:
        existing_category = (
            db.query(ResourceCategory)
            .filter(
                ResourceCategory.name == data.name,
                ResourceCategory.id != category.id
            )
            .first()
        )

        if existing_category:
            raise ValueError("Category name already exists")

        category.name = data.name

    if data.description is not None:
        category.description = data.description

    if data.is_active is not None:
        category.is_active = data.is_active

    if data.parent_category_id is not None:
        category.parent_category_id = data.parent_category_id

    db.commit()
    db.refresh(category)

    return category