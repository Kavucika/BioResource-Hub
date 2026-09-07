from pydantic import BaseModel


class CreateCategoryRequest(BaseModel):
    name: str
    description: str | None = None
    parent_category_id: str | None = None


class UpdateCategoryRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    parent_category_id: str | None = None