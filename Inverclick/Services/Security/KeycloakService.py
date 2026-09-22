# KeycloakService.py
# CA4: toda la comunicación con el servidor Keycloak vive AQUÍ y solo aquí.
#
# Esta clase no sabe nada de usuarios, roles ni base de datos: solo sabe
# construir la URL de login de Keycloak, cambiar un "code" por tokens y
# pedir los datos del usuario. Quien decide qué hacer con esos datos
# (crear el usuario, asignar rol, emitir el JWT) es SsoLoginService.
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

REQUEST_TIMEOUT_SECONDS = 10


class KeycloakError(Exception):
    """Error al hablar con Keycloak. 'kind' indica qué falló para que
    la capa de arriba lo traduzca a una respuesta HTTP adecuada."""

    NOT_CONFIGURED = "not_configured"
    INVALID_CODE = "invalid_code"
    UNAVAILABLE = "unavailable"

    def __init__(self, kind: str, message: str):
        super().__init__(message)
        self.kind = kind
        self.message = message


class KeycloakService:
    def __init__(
        self,
        server_url: str | None = None,
        realm: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        redirect_uri: str | None = None,
    ):
        # Si no se pasan valores, se leen de las variables del archivo .env
        self.server_url = (server_url or os.getenv(
            "KEYCLOAK_URL", "")).rstrip("/")
        self.realm = realm or os.getenv("KEYCLOAK_REALM", "")
        self.client_id = client_id or os.getenv("KEYCLOAK_CLIENT_ID", "")
        self.client_secret = client_secret or os.getenv(
            "KEYCLOAK_CLIENT_SECRET", "")
        self.redirect_uri = redirect_uri or os.getenv(
            "KEYCLOAK_REDIRECT_URI", "")

    # --- URLs de Keycloak (OpenID Connect) ---

    def _realm_url(self) -> str:
        return f"{self.server_url}/realms/{self.realm}/protocol/openid-connect"

    def _ensure_configured(self) -> None:
        missing = [
            name for name, value in (
                ("KEYCLOAK_URL", self.server_url),
                ("KEYCLOAK_REALM", self.realm),
                ("KEYCLOAK_CLIENT_ID", self.client_id),
                ("KEYCLOAK_REDIRECT_URI", self.redirect_uri),
            ) if not value
        ]
        if missing:
            raise KeycloakError(
                KeycloakError.NOT_CONFIGURED,
                f"Falta configurar Keycloak en el .env: {', '.join(missing)}"
            )

    # --- Operaciones ---

    def get_authorization_url(self, state: str | None = None) -> str:
        """URL a la que se redirige al usuario para que inicie sesión en Keycloak."""
        self._ensure_configured()
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "scope": "openid email profile",
            "redirect_uri": self.redirect_uri,
        }
        if state:
            params["state"] = state
        return f"{self._realm_url()}/auth?{urllib.parse.urlencode(params)}"

    def exchange_code_for_tokens(self, code: str) -> dict[str, Any]:
        """Cambia el 'code' que Keycloak entrega en el callback por los tokens."""
        self._ensure_configured()
        form = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
        }
        if self.client_secret:
            form["client_secret"] = self.client_secret

        request = urllib.request.Request(
            f"{self._realm_url()}/token",
            data=urllib.parse.urlencode(form).encode("utf-8"),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        return self._send(request, error_kind_on_4xx=KeycloakError.INVALID_CODE)

    def get_user_info(self, access_token: str) -> dict[str, Any]:
        """Pide a Keycloak los datos del usuario (sub, email, nombre...)."""
        self._ensure_configured()
        request = urllib.request.Request(
            f"{self._realm_url()}/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            method="GET",
        )
        return self._send(request, error_kind_on_4xx=KeycloakError.INVALID_CODE)

    # --- Utilidad interna ---

    @staticmethod
    def _send(request: urllib.request.Request, error_kind_on_4xx: str) -> dict[str, Any]:
        try:
            with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if 400 <= e.code < 500:
                raise KeycloakError(
                    error_kind_on_4xx, f"Keycloak rechazó la solicitud ({e.code})")
            raise KeycloakError(
                KeycloakError.UNAVAILABLE, f"Keycloak respondió con error ({e.code})")
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            raise KeycloakError(
                KeycloakError.UNAVAILABLE, f"No se pudo contactar a Keycloak: {e}")
