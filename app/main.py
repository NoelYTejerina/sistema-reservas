# main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import auth, users, resources, categories, reservations  

app = FastAPI()

# Endpoint raíz para comprobar que la API funciona
@app.get("/")
def root():
    return {"message": "API Sistema de Reservas funcionando correctamente"}

# Endpoint para manejar errores globales
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Captura errores inesperados y devuelve un mensaje uniforme.
    No reemplaza los HTTPException normales.
    """
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"},
    )

# Registrar router de autenticación
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(resources.router) 
app.include_router(categories.router)
app.include_router(reservations.router)