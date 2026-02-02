# app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.schemas.auth import LoginRequest
from app.core.security import hash_password
from app.dependencies.auth import get_current_user, get_current_admin

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# -------------------------
# Perfil del usuario autenticado
# -------------------------
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# -------------------------
# Actualizar mi propio usuario (USER)
# -------------------------
@router.put("/me/update", response_model=UserResponse)
def update_me(
    data: LoginRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validar email duplicado
    existing = db.query(User).filter(
        User.email == data.email,
        User.id != current_user.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="El email ya está en uso")

    current_user.email = data.email
    current_user.hashed_password = hash_password(data.password)

    db.commit()
    db.refresh(current_user)
    return current_user


# -------------------------
# Listar usuarios (ADMIN)
# -------------------------
@router.get("/", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    return db.query(User).all()


# -------------------------
# Obtener usuario por ID (ADMIN)
# -------------------------
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


# -------------------------
# Actualizar usuario por ID (ADMIN)
# -------------------------
@router.put("/{user_id}/update", response_model=UserResponse)
def update_user(
    user_id: int,
    data: LoginRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Validar email duplicado
    existing = db.query(User).filter(
        User.email == data.email,
        User.id != user_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="El email ya está en uso")

    user.email = data.email
    user.hashed_password = hash_password(data.password)

    db.commit()
    db.refresh(user)
    return user


# -------------------------
# Eliminar usuario (ADMIN)
# -------------------------
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(user)
    db.commit()
    return
