# app/schemas/resource_category.py
from pydantic import BaseModel

class ResourceCategoryCreate(BaseModel):
    name: str

class ResourceCategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
