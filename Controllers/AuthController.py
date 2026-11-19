from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from Repositories.database import get_db
from Repositories.UsersLoginRepository import UsersLoginRepository
from Repositories.UsuariosRepository import UsersRepository
from Repositories.UsersRoleRepository import UsersRoleRepository
from Services.Security.KeycloakService import KeycloakService
from Services.Impl.SsoLoginService import SsoLoginService
from Services.Security.JWTHandler import create_access_token
from Utils.HttpResponses.ssoHttpResponses import SsoHttpResponses
from Models.users_login import TokenResponseSchema

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_sso_login_service(db: Session = Depends(get_db)) -> SsoLoginService:
    keycloak = KeycloakService()
    login_repository = UsersLoginRepository(db)
    users_repository = UsersRepository(db)
    roles_repository = UsersRoleRepository(db)
    http_responses = SsoHttpResponses()
    return SsoLoginService(keycloak, login_repository, users_repository, roles_repository, http_responses)


@router.get("/keycloak/login")
def keycloak_login(sso: SsoLoginService = Depends(get_sso_login_service)):
    """
    Redirige al usuario a la pantalla de login de Keycloak.
    """
    url = sso.get_authorization_url()
    return RedirectResponse(url)


@router.get("/keycloak/callback", response_model=TokenResponseSchema)
def keycloak_callback(code: str, sso: SsoLoginService = Depends(get_sso_login_service)):
    """
    Keycloak redirige aquí después de que el usuario inicia sesión.
    CA2: busca o crea el usuario local, asigna rol.
    Genera el MISMO tipo de JWT que el login local.
    """
    login_data, role_name, constructora_id = sso.authenticate_with_code(code)

    token_data = {
        "sub": str(login_data.user_id),
        "user_login": login_data.user_login,
        "role": role_name,
    }
    if constructora_id is not None:
        token_data["constructora_id"] = constructora_id

    access_token = create_access_token(token_data)
    return TokenResponseSchema(access_token=access_token)
