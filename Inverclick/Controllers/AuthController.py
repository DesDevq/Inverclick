from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from Repositories.database import get_db
from Services.Security import KeycloakService
from Services.Security.JWTHandler import create_access_token
from Models.users_login import TokenResponseSchema

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/keycloak/login")
def keycloak_login():
    """
    Redirige al usuario a la pantalla de login de Keycloak.
    """
    url = KeycloakService.get_keycloak_login_url()
    return RedirectResponse(url)


@router.get("/keycloak/callback", response_model=TokenResponseSchema)
def keycloak_callback(code: str, db: Session = Depends(get_db)):
    """
    Keycloak redirige aquí después de que el usuario inicia sesión,
    mandando un 'code' en la URL. Con ese code:
    1. Lo cambiamos por un token real de Keycloak
    2. Preguntamos quién es el usuario (email, external_id)
    3. Buscamos o creamos ese usuario en NUESTRA base de datos (CA2)
    4. Generamos NUESTRO propio JWT y se lo devolvemos
    """
    token_data = KeycloakService.exchange_code_for_token(code)
    userinfo = KeycloakService.get_userinfo(token_data["access_token"])

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
