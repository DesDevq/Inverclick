# SsoLoginService.py
# CA2: qué hacer con un usuario que inicia sesión vía Keycloak.
#
# Este servicio orquesta: pide los datos a KeycloakService (CA4), busca o
# crea el usuario local, le asigna el rol base y devuelve lo mismo que el
# login local (login, rol, constructora_id) para que el controlador emita
# el MISMO token JWT de siempre.
from Repositories.UsersLoginRepository import UsersLoginRepository
from Repositories.UsuariosRepository import UsersRepository
from Repositories.UsersRoleRepository import UsersRoleRepository
from Models.users import UserDTO
from Models.users_login import UserLoginDTO
from Models.users_role import UserRoleDTO
from Services.Security.KeycloakService import KeycloakService, KeycloakError
from Utils.enums import IdentificationTypeEnum
from Utils.HttpResponses.ssoHttpResponses import SsoHttpResponses

KEYCLOAK_PROVIDER = "keycloak"
# Rol que reciben automáticamente los usuarios creados por primera vez vía Keycloak.
DEFAULT_ROLE_NAME = "Usuario"


class SsoLoginService:
    def __init__(
        self,
        keycloak: KeycloakService,
        login_repository: UsersLoginRepository,
        users_repository: UsersRepository,
        roles_repository: UsersRoleRepository,
        http_responses: SsoHttpResponses,
    ):
        self.keycloak = keycloak
        self.login_repository = login_repository
        self.users_repository = users_repository
        self.roles_repository = roles_repository
        self.http_responses = http_responses

    def get_authorization_url(self, state: str | None = None) -> str:
        try:
            return self.keycloak.get_authorization_url(state)
        except KeycloakError as e:
            raise self._translate(e)

    def authenticate_with_code(self, code: str) -> tuple[UserLoginDTO, str | None, int | None]:
        """Devuelve (login, nombre_del_rol, constructora_id): igual que el login local."""
        user_info = self._fetch_user_info(code)

        external_id = user_info.get("sub")
        email = user_info.get("email")
        if not external_id or not email:
            raise self.http_responses.error_email_missing()

        login = self.login_repository.get_by_external_id(
            KEYCLOAK_PROVIDER, external_id)

        if login is None:
            user = self.users_repository.get_by_email(email)
            if user is None:
                # CA2: primer ingreso SSO -> se crea el perfil local automáticamente
                user = self._create_user_from_keycloak(user_info)
                login = self._create_keycloak_login(user, email, external_id)
            else:
                # El correo ya existía en Inverclick: se enlaza esa cuenta.
                # Solo se permite si Keycloak confirma que el correo es del usuario,
                # para que nadie se apropie de una cuenta ajena registrándose con su correo.
                if not user_info.get("email_verified"):
                    raise self.http_responses.error_email_not_verified()
                login = self.login_repository.get_by_user_id(user.id)
                if login is None:
                    login = self._create_keycloak_login(
                        user, email, external_id)
                elif not login.external_id:
                    login = self.login_repository.update(
                        login.id, {"external_id": external_id})

        if not login.active:
            raise self.http_responses.error_account_inactive()

        user = self.users_repository.get_by_id(login.user_id)
        return (login, *self._resolve_role_and_constructora(user))

    # --- Pasos internos ---

    def _fetch_user_info(self, code: str) -> dict:
        try:
            tokens = self.keycloak.exchange_code_for_tokens(code)
            return self.keycloak.get_user_info(tokens["access_token"])
        except KeycloakError as e:
            raise self._translate(e)
        except KeyError:
            raise self.http_responses.error_keycloak_invalid_code()

    def _translate(self, error: KeycloakError):
        if error.kind == KeycloakError.NOT_CONFIGURED:
            return self.http_responses.error_keycloak_not_configured(error.message)
        if error.kind == KeycloakError.INVALID_CODE:
            return self.http_responses.error_keycloak_invalid_code()
        return self.http_responses.error_keycloak_unavailable()

    def _get_or_create_default_role(self) -> UserRoleDTO:
        role = self.roles_repository.get_by_role(DEFAULT_ROLE_NAME)
        if role is None:
            # Sin módulos: el usuario nuevo no accede a nada protegido hasta
            # que un administrador le habilite módulos a este rol.
            role = self.roles_repository.create(
                UserRoleDTO(role=DEFAULT_ROLE_NAME, modules=[]))
        return role

    def _create_user_from_keycloak(self, user_info: dict) -> UserDTO:
        email = user_info["email"]
        role = self._get_or_create_default_role()
        user = UserDTO(
            name=(user_info.get("given_name")
                  or user_info.get("preferred_username")
                  or email.split("@")[0])[:100],
            last_name=(user_info.get("family_name") or "-")[:100],
            email=email[:100],
            # Keycloak no entrega documento de identidad: quedan valores
            # provisionales que el usuario puede completar después en su perfil.
            identification=f"KC-{user_info['sub']}"[:100],
            identification_type=IdentificationTypeEnum.CC,
            desired_description="Perfil creado automáticamente vía Keycloak",
            user_id_role=role.id,
        )
        return self.users_repository.create(user)

    def _create_keycloak_login(self, user: UserDTO, email: str, external_id: str) -> UserLoginDTO:
        # user_login debe ser único: si el correo ya lo usa otra cuenta, se usa el ID externo.
        user_login = email
        if self.login_repository.get_by_user_login(user_login) is not None:
            user_login = f"keycloak-{external_id}"
        login = UserLoginDTO(
            user_id=user.id,
            user_login=user_login[:100],
            user_password=None,
            active=True,
            identity_provider=KEYCLOAK_PROVIDER,
            external_id=external_id,
        )
        return self.login_repository.create(login)

    def _resolve_role_and_constructora(self, user: UserDTO | None) -> tuple[str | None, int | None]:
        """Misma regla que el login local: constructora_id solo aplica al rol 'constructora'."""
        role_name = None
        constructora_id = None
        if user and user.user_id_role:
            role = self.roles_repository.get_by_id(user.user_id_role)
            if role:
                role_name = role.role
                if role_name == "constructora":
                    constructora_id = getattr(user, "constructora_id", None)
        return role_name, constructora_id
