from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from Repositories.database import get_db
from Services.Security.KeycloakService import KeycloakService, KeycloakError
from Services.Security.JWTHandler import create_access_token
from Models.users_login import TokenResponseSchema

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_keycloak_service() -> KeycloakService:
    return KeycloakService()


@router.get("/keycloak/login")
def keycloak_login(keycloak: KeycloakService = Depends(get_keycloak_service)):
    """
    Redirige al usuario a la pantalla de login de Keycloak.
    """
    url = keycloak.get_authorization_url()
    return RedirectResponse(url)


@router.get("/keycloak/callback", response_model=TokenResponseSchema)
def keycloak_callback(
    code: str,
    db: Session = Depends(get_db),
    keycloak: KeycloakService = Depends(get_keycloak_service)
):
    """
    Keycloak redirige aquí después de que el usuario inicia sesión,
    mandando un 'code' en la URL. Con ese code:
    1. Lo cambiamos por un token real de Keycloak
    2. Preguntamos quién es el usuario (email, external_id)
    3. Buscamos o creamos ese usuario en NUESTRA base de datos (CA2)
    4. Generamos NUESTRO propio JWT y se lo devolvemos
    """
    try:
        token_data = keycloak.exchange_code_for_tokens(code)
        userinfo = keycloak.get_user_info(token_data["access_token"])
    except KeycloakError as e:
        status_map = {
            KeycloakError.NOT_CONFIGURED: 500,
            KeycloakError.INVALID_CODE: 400,
            KeycloakError.UNAVAILABLE: 503,
        }
        raise HTTPException(status_code=status_map.get(
            e.kind, 500), detail=e.message)

    email = userinfo.get("email")
    external_id = userinfo.get("sub")

    # --- PUNTO DE INTEGRACIÓN (CA2) ---
    # Aquí se llama a la función
    # login_data, role_name = auth_service.find_or_create_from_keycloak(email, external_id)
    #

    # <-- reemplazar cuando esté la función en usersloginservice
    login_data, role_name = None, None

    jwt_payload = {
        "sub": str(login_data.user_id),
        "user_login": login_data.user_login,
        "role": role_name,
    }
    access_token = create_access_token(jwt_payload)

    return TokenResponseSchema(access_token=access_token)
