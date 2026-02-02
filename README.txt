# 🗂️ Sistema de Reservas – API REST con FastAPI

  API REST profesional desarrollada con FastAPI, SQLAlchemy, Alembic y MySQL, que permite gestionar recursos reservables (salas, equipos, vehículos, aulas…) y las reservas asociadas a ellos.
  Incluye autenticación JWT, autorización por roles, validaciones de disponibilidad y CRUD completo de usuarios, recursos, categorías y reservas.

-----

# 🚀 Características principales

  ## 🔐 Autenticación y seguridad

    - Login y registro de usuarios

    - Tokens JWT con expiración

    - Hashing de contraseñas con bcrypt

    - Roles: user y admin

    - Protección de rutas mediante dependencias (get_current_user, get_current_admin)

  ## 👤 Usuarios

    - Ver perfil propio

    - Actualizar email y contraseña

    - Listar, ver, actualizar y eliminar usuarios (solo admin)

  ## 📦 Recursos
    - Crear, listar, actualizar y eliminar recursos (admin)

    - Activar/desactivar recursos

    - Asociar categorías

    - Añadir y eliminar campos personalizados

  ## 🏷️ Categorías
    - Crear, listar, actualizar y eliminar categorías (admin)

  ## 📅 Reservas
    - Crear reservas

    - Listar reservas

    - Obtener reserva por ID

    - Cancelar reservas

    - Validación de solapamientos

    - Validación de disponibilidad

    - Permisos por rol (user/admin)

  ## 🧱 Arquitectura
    - FastAPI modular (routers, models, schemas, dependencies)

    - SQLAlchemy ORM

    - Migraciones con Alembic

    - Documentación automática con Swagger

-----

# 📦 Tecnologías utilizadas
  - Python 3

  - FastAPI

  - SQLAlchemy

  - Alembic

  - MySQL

  - Pydantic

  - python‑jose (JWT)

  - Uvicorn

-----

# 📁 Estructura del repositorio

sistema-reservas/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── core/
│   │   └── security.py
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   └── dependencies/
│
├── docs/
│   ├── Documentacion_Sistema_Reservas.pdf
│   ├── index.html
│   └── capturas/
│       ├── login.png
│       ├── crear_recurso.png
│       ├── crear_reserva.png
│       └── cancelar_reserva.png
├── alembic/
├── alembic.ini
├── requirements.txt
└── README.md

-----

# 🛠️ Instalación y ejecución

1️⃣ Clonar el repositorio
git clone https://github.com/NoelYTejerina/sistema-reservas.git
cd sistema-reservas

2️⃣ Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

3️⃣ Instalar dependencias
pip install -r requirements.txt

4️⃣ Configurar MySQL
CREATE USER 'fastapi'@'localhost' IDENTIFIED BY 'Examen123';
CREATE DATABASE sistema_reservas;
GRANT ALL PRIVILEGES ON sistema_reservas.* TO 'fastapi'@'localhost';
FLUSH PRIVILEGES;

5️⃣ Ejecutar migraciones
alembic upgrade head

6️⃣ Iniciar el servidor
uvicorn app.main:app --reload

📘 Documentación interactiva de la API (Swagger)
http://localhost:8000/docs
Panel para probar Endpoints

-----

# 📚 Documentación completa
  La documentación técnica del proyecto está disponible en:
  /docs/Documentacion_Sistema_Reservas.pdf
  Incluye:

    - Arquitectura

    - Modelos y relaciones

    - Reglas de negocio

    - Seguridad JWT

    - Migraciones

    - Endpoints

    - Validaciones

-----

# 📡 Endpoints principales

  ## 🔑 Autenticación
    - POST /auth/register

    - POST /auth/login

  ## 👤 Usuarios
    - GET /users/me

    - PUT /users/me/update

    - GET /users/

    - GET /users/{id}

    - PUT /users/{id}/update

    - DELETE /users/{id}

  ## 📦 Recursos
    - POST /resources/

    - GET /resources/

    - GET /resources/{id}

    - PUT /resources/{id}

    - DELETE /resources/{id}

    - POST /resources/{id}/custom-fields

    - DELETE /resources/{id}/custom-fields/{field_id}

  ## 🏷️ Categorías
    - POST /categories/

    - GET /categories/

    - PUT /categories/{id}

    - DELETE /categories/{id}

  ## 📅 Reservas
    - POST /reservations/

    - GET /reservations/

    - GET /reservations/{id}

    - DELETE /reservations/{id}

  ##🧠 Validaciones y reglas de negocio
    - Un recurso solo puede reservarse si está activo

    - start_time < end_time

    - No puede haber solapamiento de reservas

    - Un usuario solo puede cancelar sus reservas

    - Un admin puede cancelar cualquier reserva

    - Emails únicos

    - Categorías sin duplicados

    - Recursos y usuarios deben existir

  #🎨 Demo visual del proyecto
📸 https://NoelYTejerina.github.io/sistema-reservas/demo


# 🚀 Extensiones futuras
  - Campos personalizados avanzados
  - Tipos de campo
  - Validaciones dinámicas
  - Formularios configurables
  - Calendario visual
  - Vista mensual/semanal
  - Integración con FullCalendar
  - Bloqueos en tiempo real
  - Notificaciones por email
  - Confirmación de reserva
  - Recordatorios
  - Cancelaciones
  - Panel de administración (Dashboard)
  - Gestión visual de recursos
  - Estadísticas
  - ....

## 📄 Licencia

Este proyecto se distribuye bajo licencia **MIT**, lo que permite:

- Copiar  
- Modificar  
- Distribuir  
- Usar comercialmente  

Siempre que se mantenga el aviso de copyright.

---

🤝 Autor
Noel Y. Tejerina  
GitHub: https://github.com/NoelYTejerina
