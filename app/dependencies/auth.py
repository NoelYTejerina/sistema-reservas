# app/dependencies/auth.py

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.security import SECRET_KEY, ALGORITHM
from app.database import get_db
from app.models.user import User

oauth2_scheme = HTTPBearer()


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    print(">>> get_current_user SE ESTÁ EJECUTANDO")
    print(">>> TOKEN RECIBIDO:", token)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        print(">>> PAYLOAD DECODIFICADO:", payload)

        user_id_str = payload.get("sub")
        print(">>> USER_ID OBTENIDO DEL TOKEN (str):", user_id_str)

        if user_id_str is None:
            print(">>> USER_ID ES NONE → 401")
            raise credentials_exception

        # Convertir a int
        try:
            user_id = int(user_id_str)
        except ValueError:
            print(">>> USER_ID NO ES UN INT VÁLIDO → 401")
            raise credentials_exception

        print(">>> USER_ID CONVERTIDO A INT:", user_id)

    except JWTError as e:
        print(">>> JWTError EN DECODE:", e)
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    print(">>> USER EN BD:", user)

    if user is None:
        print(">>> USER ES NONE → 401")
        raise credentials_exception

    return user


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador",
        )
    return current_user
