from pydantic import BaseModel

# Esquema para mostrar usuarios (respuesta)
class UserResponse(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        from_attributes = True  # Permite convertir desde SQLAlchemy
