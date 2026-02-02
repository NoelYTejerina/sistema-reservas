# app/core/security.py

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

# Clave secreta para firmar los tokens JWT
# En producción debe venir de variables de entorno
SECRET_KEY = "super-secret-key-change-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Contexto de Passlib para hashear y verificar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
	"""Devuelve el hash seguro de una contraseña en texto plano."""
	return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
	"""Verifica si una contraseña en texto plano coincide con su hash."""
	return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
	"""
	Crea un token JWT firmado con SECRET_KEY.
	`data` suele incluir el identificador del usuario (sub).
	"""
	to_encode = data.copy()
	expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
	to_encode.update({"exp": expire})
	return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
