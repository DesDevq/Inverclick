from fastapi import HTTPException


class SsoHttpResponses:
    @staticmethod
    def error_keycloak_not_configured(detail: str) -> HTTPException:
        return HTTPException(status_code=500, detail=detail)

    @staticmethod
    def error_keycloak_invalid_code() -> HTTPException:
        return HTTPException(
            status_code=401,
            detail="El código de autorización de Keycloak es inválido o expiró")

    @staticmethod
    def error_keycloak_unavailable() -> HTTPException:
        return HTTPException(
            status_code=502,
            detail="No se pudo comunicar con el servidor Keycloak")

    @staticmethod
    def error_email_missing() -> HTTPException:
        return HTTPException(
            status_code=400,
            detail="Keycloak no entregó un correo para este usuario")

    @staticmethod
    def error_email_not_verified() -> HTTPException:
        return HTTPException(
            status_code=403,
            detail="Ya existe una cuenta con este correo, pero Keycloak no lo tiene verificado")

    @staticmethod
    def error_account_inactive() -> HTTPException:
        return HTTPException(status_code=403, detail="La cuenta está inactiva")
