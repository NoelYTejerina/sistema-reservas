# app/routers/categories.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.resource_category import ResourceCategory
from app.schemas.resource_category import (
    ResourceCategoryResponse,
    ResourceCategoryCreate,
)
from app.dependencies.auth import get_current_admin

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


# -------------------------
# Crear categoría (ADMIN)
# -------------------------
@router.post(
    "/", 
    response_model=ResourceCategoryResponse, 
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    data: ResourceCategoryCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    existing = db.query(ResourceCategory).filter(ResourceCategory.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="La categoría ya existe")

    category = ResourceCategory(name=data.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


# -------------------------
# Listar categorías (PÚBLICO)
# -------------------------
@router.get("/", response_model=List[ResourceCategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return db.query(ResourceCategory).all()


# -------------------------
# Actualizar categoría (ADMIN)
# -------------------------
@router.put("/{category_id}", response_model=ResourceCategoryResponse)
def update_category(
    category_id: int,
    data: ResourceCategoryCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    category = db.query(ResourceCategory).filter(ResourceCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    # Evitar duplicados
    existing = db.query(ResourceCategory).filter(
        ResourceCategory.name == data.name,
        ResourceCategory.id != category_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe otra categoría con ese nombre")

    category.name = data.name
    db.commit()
    db.refresh(category)
    return category


# -------------------------
# Eliminar categoría (ADMIN)
# -------------------------
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    category = db.query(ResourceCategory).filter(ResourceCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    db.delete(category)
    db.commit()
    return
