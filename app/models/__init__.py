#Este archivo sirve para:
#convertir la carpeta models en un paquete Python
#importar todos los modelos para que SQLAlchemy los registre
#permitir que Alembic los detecte automáticamente


from .user import User
from .resource_category import ResourceCategory
from .resource import Resource
from .reservation import Reservation
from .custom_field import CustomField


