from fastapi import HTTPException
from fastapi.responses import JSONResponse
from Utils.HttpResponses.http_response import success_response
from Models.users_login import UserLoginDTO

class UserLoginHttpResponses:
    @staticmethod
    def success_created(loginDTO: UserLoginDTO) -> JSONResponse:
        return success_response(loginDTO, "Login de usuario creado exitosamente", 201)

    @staticmethod
    def success_get(loginDTO: UserLoginDTO) -> JSONResponse:
        return success_response(loginDTO, "Login de usuario obtenido exitosamente", 200)

    @staticmethod   
    def success_get_all(logins: list[UserLoginDTO]) -> JSONResponse:
        return success_response(logins, "Logins de usuarios obtenidos exitosamente", 200)

    @staticmethod
    def success_updated(loginDTO: UserLoginDTO) -> JSONResponse:
        return success_response(loginDTO, "Login de usuario actualizado exitosamente", 200)

    @staticmethod
    def success_deleted() -> JSONResponse:
        return success_response(None, "Login de usuario eliminado exitosamente", 200)

    @staticmethod
    def error_login_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="Login de usuario no encontrado")

    @staticmethod
    def error_user_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="Usuario no encontrado")

    @staticmethod
    def error_login_already_exists() -> HTTPException:
        return HTTPException(status_code=400, detail="El usuario de login (user_login) ya existe")

    @staticmethod
    def error_login_not_created() -> HTTPException:
        return HTTPException(status_code=400, detail="Login de usuario no creado")

    @staticmethod
    def error_invalid_credentials() -> HTTPException:
        return HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    @staticmethod
    def error_account_inactive() -> HTTPException:
        return HTTPException(status_code=403, detail="La cuenta de usuario se encuentra inactiva")

    @staticmethod
    def error_invalid_length(field: str, min_length: int, max_length: int) -> HTTPException:
        return HTTPException(status_code=400, detail=f"Longitud inválida para el campo {field}, debe tener entre {min_length} y {max_length} caracteres")

    @staticmethod
    def error_login_not_updated() -> HTTPException:
        return HTTPException(status_code=400, detail="Login de usuario no actualizado")

    @staticmethod
    def error_login_not_deleted() -> HTTPException:
        return HTTPException(status_code=400, detail="Login de usuario no eliminado")
