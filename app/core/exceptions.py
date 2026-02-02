# app/core/exceptions.py

from fastapi import HTTPException, status

def not_found(entity: str):
    """
    Error estándar para entidades no encontradas.
    Ejemplo: not_found("Recurso")
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{entity} no encontrado",
    )


def bad_request(message: str):
    """
    Error estándar para peticiones inválidas.
    """
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message,
    )


def forbidden(message: str = "No tienes permisos para realizar esta acción"):
    """
    Error estándar para acciones no permitidas.
    """
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=message,
    )


def conflict(message: str):
    """
    Error estándar para conflictos (ej: solapamiento de reservas).
    """
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=message,
    )
