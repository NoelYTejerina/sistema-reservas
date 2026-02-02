from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class CustomField(Base):
    __tablename__ = "custom_fields"

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    key = Column(String(255), nullable=False)
    value = Column(String(255), nullable=False)

    resource = relationship("Resource", back_populates="custom_fields")
