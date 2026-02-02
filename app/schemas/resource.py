from pydantic import BaseModel
from typing import Optional, List
from .custom_field import CustomFieldResponse
from .resource_category import ResourceCategoryResponse

class ResourceResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    category: Optional[ResourceCategoryResponse]
    custom_fields: List[CustomFieldResponse] = []

    class Config:
        from_attributes = True
