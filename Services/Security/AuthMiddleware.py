from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from Repositories.database import get_db
from Repositories.UsersRoleRepository import UsersRoleRepository
from Services.Security.JWTHandler import decode_access_token

security = HTTPBearer()


def get_current_payload(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    print(f"Token recibido: {token}")
    payload = decode_access_token(token)
    print(f"Payload decodificado: {payload}")

    if payload is None:
        raise HTTPException(
            status_code=401, detail="Token inválido o expirado")

    return payload


def require_module(module_name: str):
    def dependency(
        payload: dict = Depends(get_current_payload),
        db: Session = Depends(get_db)
    ):
        role_name = payload.get("role")
        if role_name is None:
            raise HTTPException(
                status_code=403, detail="El token no contiene un rol válido")

        roles_repository = UsersRoleRepository(db)
        role = roles_repository.get_by_role(role_name)

        if role is None:
            raise HTTPException(status_code=403, detail="Rol no encontrado")

        modules = role.modules or []

        if "All" in modules or module_name in modules:
            return payload

        raise HTTPException(
            status_code=403,
            detail=f"El rol '{role_name}' no tiene acceso al módulo '{module_name}'"
        )

    return dependency


def get_current_user_context(payload: dict = Depends(get_current_payload)) -> dict:
    return {
        "user_id": payload.get("sub"),
        "role": payload.get("role"),
        "constructora_id": payload.get("constructora_id")
    }
