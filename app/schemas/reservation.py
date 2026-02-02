# app/schemas/reservation.py

from pydantic import BaseModel
from datetime import datetime

class ReservationResponse(BaseModel):
    """
    Esquema de salida para reservas.
    Representa cómo se devuelven las reservas al cliente.
    """
    id: int
    user_id: int
    resource_id: int
    start_time: datetime
    end_time: datetime
    status: str

    class Config:
        from_attributes = True  # Permite convertir desde modelos SQLAlchemy
