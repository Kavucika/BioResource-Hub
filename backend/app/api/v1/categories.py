from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User

from app.schemas.category import (
    CreateCategoryRequest,
    UpdateCategoryRequest
)

from app.services.category_service import (
    create_category,
    get_all_categories,
    get_category,
    update_category
)


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post("")
def create(
    data: CreateCategoryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        category = create_category(db, data)

        return {
            "message": "Category created successfully",
            "category": {
                "category_id": str(category.id),
                "name": category.name,
                "description": category.description,
                "parent_category_id": (
                    str(category.parent_category_id)
                    if category.parent_category_id
                    else None
                ),
                "is_active": category.is_active
            }
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("")
def get_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    categories = get_all_categories(db)

    return {
        "count": len(categories),
        "categories": [
            {
                "category_id": str(category.id),
                "name": category.name,
                "description": category.description,
                "parent_category_id": (
                    str(category.parent_category_id)
                    if category.parent_category_id
                    else None
                ),
                "is_active": category.is_active
            }
            for category in categories
        ]
    }


@router.get("/{category_id}")
def get_single_category(
    category_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        category = get_category(db, category_id)

        return {
            "category_id": str(category.id),
            "name": category.name,
            "description": category.description,
            "parent_category_id": (
                str(category.parent_category_id)
                if category.parent_category_id
                else None
            ),
            "is_active": category.is_active
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.put("/{category_id}")
def update(
    category_id: str,
    data: UpdateCategoryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        category = update_category(
            db,
            category_id,
            data
        )

        return {
            "message": "Category updated successfully",
            "category": {
                "category_id": str(category.id),
                "name": category.name,
                "description": category.description,
                "parent_category_id": (
                    str(category.parent_category_id)
                    if category.parent_category_id
                    else None
                ),
                "is_active": category.is_active
            }
        }

    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(
                status_code=404,
                detail=str(e)
            )

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )