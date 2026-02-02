from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    is_active = Column(Boolean, default=True)

    # Relación con categoría
    category_id = Column(Integer, ForeignKey("resource_categories.id"), nullable=True)
    category = relationship("ResourceCategory", back_populates="resources")

    # Relación con reservas
    reservations = relationship("Reservation", back_populates="resource")

    # Relación con campos personalizados
    custom_fields = relationship("CustomField", back_populates="resource")
