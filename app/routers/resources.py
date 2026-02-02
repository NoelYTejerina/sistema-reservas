# app/routers/resources.py

# APIRouter = equivalente a un Controller en Symfony
from fastapi import APIRouter, Depends, HTTPException, status

# Session = equivalente a una conexión Doctrine
from sqlalchemy.orm import Session

# Tipado para listas en las respuestas
from typing import List

# Dependencia que nos da una sesión de base de datos por petición
from app.database import get_db

# Modelos SQLAlchemy (equivalentes a entidades Doctrine)
from app.models.resource import Resource
from app.models.resource_category import ResourceCategory
from app.models.custom_field import CustomField

# Schemas Pydantic = equivalentes a DTOs o Response Models
from app.schemas.resource import ResourceResponse
from app.schemas.custom_field import CustomFieldResponse

# Dependencias de autenticación (equivalentes a voters o security checks)
from app.dependencies.auth import get_current_user, get_current_admin


# Creamos un router con prefijo /resources
# Esto es como @Route("/resources") en Symfony
router = APIRouter(
    prefix="/resources",
    tags=["Resources"],
)



@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
def create_resource(
    name: str,
    description: str | None = None,
    category_id: int | None = None,
    db: Session = Depends(get_db),          # Inyección de la sesión DB
    admin=Depends(get_current_admin),       # Solo admin puede crear recursos
):
    """
    Crea un recurso nuevo.
    """

    # Si se pasa category_id, validamos que exista
    if category_id:
        category = db.query(ResourceCategory).filter(ResourceCategory.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")

    # Creamos la entidad Resource
    resource = Resource(
        name=name,
        description=description,
        category_id=category_id,
    )

    # Persistimos en la base de datos
    db.add(resource)
    db.commit()
    db.refresh(resource)  # Recarga la entidad con datos actualizados (como el ID)

    return resource



@router.get("/", response_model=List[ResourceResponse])
def list_resources(db: Session = Depends(get_db)):
    """
    Lista todos los recursos disponibles.
    Acceso público (requiere token).
    """
    resources = db.query(Resource).all()
    return resources


@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    """
    Devuelve un recurso por ID.
    """
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    return resource


@router.put("/{resource_id}", response_model=ResourceResponse)
def update_resource(
    resource_id: int,
    name: str | None = None,
    description: str | None = None,
    category_id: int | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """
    Actualiza un recurso existente.
    Solo accesible para administradores.
    """

    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

    # Validamos categoría si se envía
    if category_id:
        category = db.query(ResourceCategory).filter(ResourceCategory.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")

    # Actualizamos solo los campos enviados
    if name is not None:
        resource.name = name
    if description is not None:
        resource.description = description
    if category_id is not None:
        resource.category_id = category_id
    if is_active is not None:
        resource.is_active = is_active

    db.commit()
    db.refresh(resource)
    return resource



@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """
    Elimina un recurso por ID.
    Solo accesible para administradores.
    """
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

    db.delete(resource)
    db.commit()
    return


# ------------------------------
# CAMPOS PERSONALIZADOS
# ------------------------------

@router.post("/{resource_id}/fields", response_model=CustomFieldResponse)
def add_custom_field(
    resource_id: int,
    key: str,
    value: str,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """
    Añade un campo personalizado a un recurso.
    """
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

    field = CustomField(
        resource_id=resource_id,
        key=key,
        value=value,
    )
    db.add(field)
    db.commit()
    db.refresh(field)
    return field


@router.delete("/{resource_id}/fields/{field_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_custom_field(
    resource_id: int,
    field_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """
    Elimina un campo personalizado de un recurso.
    """
    field = db.query(CustomField).filter(
        CustomField.id == field_id,
        CustomField.resource_id == resource_id
    ).first()

    if not field:
        raise HTTPException(status_code=404, detail="Campo personalizado no encontrado")

    db.delete(field)
    db.commit()
    return
