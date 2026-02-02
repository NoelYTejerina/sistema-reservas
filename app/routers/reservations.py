# app/routers/reservations.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.reservation import Reservation
from app.models.resource import Resource
from app.schemas.reservation import ReservationResponse
from app.dependencies.auth import get_current_user, get_current_admin

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"],
)


@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(
    resource_id: int,
    start_time: datetime,
    end_time: datetime,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Crea una reserva aplicando todas las reglas de negocio:
    - recurso existe
    - recurso activo
    - fechas válidas
    - no solapamiento
    """

    # Validar recurso
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

    if not resource.is_active:
        raise HTTPException(status_code=400, detail="El recurso no está disponible")

    # Validar fechas
    if start_time >= end_time:
        raise HTTPException(status_code=400, detail="La fecha de inicio debe ser menor que la de fin")

    # Validar solapamiento
    overlapping = db.query(Reservation).filter(
        Reservation.resource_id == resource_id,
        Reservation.start_time < end_time,
        Reservation.end_time > start_time,
    ).first()

    if overlapping:
        raise HTTPException(status_code=409, detail="El recurso ya está reservado en ese intervalo")

    # Crear reserva
    reservation = Reservation(
        user_id=current_user.id,
        resource_id=resource_id,
        start_time=start_time,
        end_time=end_time,
        status="active",
    )

    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return reservation


@router.get("/", response_model=List[ReservationResponse])
def list_reservations(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Lista reservas:
    - Admin: todas
    - Usuario: solo las suyas
    """
    if current_user.role == "admin":
        return db.query(Reservation).all()

    return db.query(Reservation).filter(Reservation.user_id == current_user.id).all()


@router.get("/{reservation_id}", response_model=ReservationResponse)
def get_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Devuelve una reserva por ID.
    - Admin: puede ver cualquier reserva
    - Usuario: solo las suyas
    """
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    if current_user.role != "admin" and reservation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver esta reserva")

    return reservation


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Cancela una reserva.
    - Admin: puede cancelar cualquier reserva
    - Usuario: solo las suyas
    """
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    if current_user.role != "admin" and reservation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para cancelar esta reserva")

    db.delete(reservation)
    db.commit()
    return
