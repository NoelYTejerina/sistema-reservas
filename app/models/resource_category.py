# app/models/resource_category.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class ResourceCategory(Base):
    __tablename__ = "resource_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)

    # Relación inversa: una categoría tiene muchos recursos
    resources = relationship("Resource", back_populates="category")
