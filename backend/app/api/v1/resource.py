from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User

from app.schemas.resource import (
    CreateResourceRequest,
    UpdateResourceRequest,
    ResourceResponse
)

from app.services.resource_service import (
    create_resource,
    get_all_resources,
    get_resource,
    update_resource,
    delete_resource
)


router = APIRouter(
    prefix="/resources",
    tags=["Resources"]
)


def resource_to_response(resource):
    return {
        "resource_id": resource.id,
        "user_id": resource.user_id,
        "name": resource.name,
        "description": resource.description,
        "category_id": resource.category_id,
        "quantity": resource.quantity,
        "unit": resource.unit,
        "condition": resource.condition,
        "quality_description": resource.quality_description,
        "asking_price": resource.asking_price,
        "currency": resource.currency,
        "location_id": resource.location_id,
        "status": resource.status,
        "created_at": resource.created_at,
        "updated_at": resource.updated_at,
        "expires_at": resource.expires_at
    }


@router.post(
    "",
    response_model=ResourceResponse
)
def create(
    data: CreateResourceRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        resource = create_resource(
            db,
            current_user.id,
            data
        )

        return resource_to_response(resource)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("")
def get_resources(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resources = get_all_resources(db)

    return {
        "count": len(resources),
        "resources": [
            resource_to_response(resource)
            for resource in resources
        ]
    }


@router.get(
    "/{resource_id}",
    response_model=ResourceResponse
)
def get_single_resource(
    resource_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        resource = get_resource(
            db,
            resource_id
        )

        return resource_to_response(resource)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.put(
    "/{resource_id}",
    response_model=ResourceResponse
)
def update(
    resource_id: UUID,
    data: UpdateResourceRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        resource = update_resource(
            db,
            resource_id,
            current_user.id,
            data
        )

        return resource_to_response(resource)

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

    except PermissionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e)
        )


@router.delete(
    "/{resource_id}"
)
def delete(
    resource_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        resource = delete_resource(
            db,
            resource_id,
            current_user.id
        )

        return {
            "message": "Resource cancelled successfully",
            "resource_id": str(resource.id),
            "status": resource.status
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e)
        )