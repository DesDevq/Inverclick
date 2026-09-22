import os
import httpx
from urllib.parse import urlencode

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
KEYCLOAK_REDIRECT_URI = os.getenv("KEYCLOAK_REDIRECT_URI")


def get_keycloak_login_url() -> str:
    """
    Arma la URL a la que hay que redirigir al usuario para que inicie
    sesión en la pantalla de Keycloak.
    """
    base_url = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth"
    params = {
        "client_id": KEYCLOAK_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": KEYCLOAK_REDIRECT_URI,
        "scope": "openid email profile",
    }
    return f"{base_url}?{urlencode(params)}"


def exchange_code_for_token(code: str) -> dict:
    """
    Intercambia el 'code' que Keycloak mandó en el callback por un
    access_token real de Keycloak (usando el client_secret, por eso
    esto SOLO puede hacerse desde el backend, nunca desde el navegador).
    """
    token_url = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": KEYCLOAK_REDIRECT_URI,
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": KEYCLOAK_CLIENT_SECRET,
    }

    response = httpx.post(token_url, data=data)
    if response.status_code != 200:
        raise Exception(
            f"Error al intercambiar el código con Keycloak: {response.text}")

    return response.json()


def get_userinfo(access_token: str) -> dict:
    """
    Con el access_token de Keycloak, pregunta quién es el usuario:
    su email, nombre, y el 'sub' (external_id único que Keycloak
    le asigna a cada usuario).
    """
    userinfo_url = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = httpx.get(userinfo_url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            f"Error al obtener userinfo de Keycloak: {response.text}")

    return response.json()
