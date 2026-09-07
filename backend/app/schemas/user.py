from pydantic import BaseModel


class UpdateProfileRequest(BaseModel):
    full_name: str | None = None
    user_type: str | None = None
    organization_name: str | None = None
    bio: str | None = None
    profile_image_url: str | None = None