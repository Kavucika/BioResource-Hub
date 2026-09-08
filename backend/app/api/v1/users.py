from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db

from app.models.user import User
from app.models.user_profile import UserProfile

from app.schemas.user import UpdateProfileRequest

from app.models.location import Location
from app.schemas.location import LocationRequest


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == current_user.id)
        .first()
    )

    return {
        "user_id": str(current_user.id),
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,

        "profile": {
            "user_type": profile.user_type if profile else None,
            "organization_name": (
                profile.organization_name
                if profile else None
            ),
            "bio": profile.bio if profile else None,
            "profile_image_url": (
                profile.profile_image_url
                if profile else None
            )
        }
    }


@router.put("/me")
def update_my_profile(
    data: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == current_user.id)
        .first()
    )

    if profile is None:
        profile = UserProfile(
            user_id=current_user.id
        )
        db.add(profile)

    if data.full_name is not None:
        current_user.full_name = data.full_name

    if data.user_type is not None:
        profile.user_type = data.user_type

    if data.organization_name is not None:
        profile.organization_name = data.organization_name

    if data.bio is not None:
        profile.bio = data.bio

    if data.profile_image_url is not None:
        profile.profile_image_url = data.profile_image_url

    db.commit()

    db.refresh(current_user)
    db.refresh(profile)

    return {
        "message": "Profile updated successfully",
        "user": {
            "user_id": str(current_user.id),
            "email": current_user.email,
            "full_name": current_user.full_name,
            "role": current_user.role
        },
        "profile": {
            "user_type": profile.user_type,
            "organization_name": profile.organization_name,
            "bio": profile.bio,
            "profile_image_url": profile.profile_image_url
        }
    }


@router.put("/me/location")
def update_my_location(
    data: LocationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == current_user.id)
        .first()
    )

    if profile is None:
        profile = UserProfile(
            user_id=current_user.id
        )
        db.add(profile)
        db.flush()

    if profile.address_id:
        location = (
            db.query(Location)
            .filter(Location.id == profile.address_id)
            .first()
        )

        if location is None:
            location = Location()
            db.add(location)
    else:
        location = Location()
        db.add(location)

    location.address_line = data.address_line
    location.village = data.village
    location.city = data.city
    location.district = data.district
    location.state = data.state
    location.country = data.country
    location.pincode = data.pincode
    location.latitude = data.latitude
    location.longitude = data.longitude

    db.flush()

    profile.address_id = location.id

    db.commit()

    db.refresh(location)
    db.refresh(profile)

    return {
        "message": "Location updated successfully",
        "location": {
            "location_id": str(location.id),
            "address_line": location.address_line,
            "village": location.village,
            "city": location.city,
            "district": location.district,
            "state": location.state,
            "country": location.country,
            "pincode": location.pincode,
            "latitude": float(location.latitude)
            if location.latitude is not None else None,
            "longitude": float(location.longitude)
            if location.longitude is not None else None
        }
    }