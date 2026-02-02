# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session

# URL de conexión a MySQL
DATABASE_URL = "mysql+pymysql://fastapi:Examen123@localhost:3306/sistema_reservas"

# Engine principal de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Muestra las consultas SQL en consola (útil en desarrollo)
)

# Creador de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Clase base para los modelos
Base = declarative_base()


def get_db():
    """
    Dependencia de FastAPI que proporciona una sesión de base de datos.
    Se asegura de cerrar la sesión después de cada petición.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
