from pydantic import BaseModel

class CustomFieldResponse(BaseModel):
    id: int
    key: str
    value: str

    class Config:
        from_attributes = True
