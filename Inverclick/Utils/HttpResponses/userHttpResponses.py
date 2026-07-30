from fastapi import HTTPException
from fastapi.responses import JSONResponse
from Utils.HttpResponses.http_response import success_response
from Models.users import UserDTO

class UserHttpResponses:
    @staticmethod
    def success_created(userDTO: UserDTO) -> JSONResponse:
        return success_response(userDTO, "Usuario creado exitosamente", 201)

    @staticmethod
    def success_get(userDTO: UserDTO) -> JSONResponse:
        return success_response(userDTO, "Usuario obtenido exitosamente", 200)

    @staticmethod   
    def success_get_all(users: list[UserDTO]) -> JSONResponse:
        return success_response(users, "Usuarios obtenidos exitosamente", 200)

    @staticmethod
    def success_updated(userDTO: UserDTO) -> JSONResponse:
        return success_response(userDTO, "Usuario actualizado exitosamente", 200)

    @staticmethod
    def success_deleted() -> JSONResponse:
        return success_response(None, "Usuario eliminado exitosamente", 200)

    @staticmethod
    def error_user_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="Usuario no encontrado")

    @staticmethod
    def error_user_already_exists() -> HTTPException:
        return HTTPException(status_code=400, detail="Usuario ya existe")

    @staticmethod
    def error_user_not_created() -> HTTPException:
        return HTTPException(status_code=400, detail="Usuario no creado")

    @staticmethod
    def error_country_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="País no encontrado")

    @staticmethod
    def error_invalid_length(field: str, min_length: int, max_length: int) -> HTTPException:
        return HTTPException(status_code=400, detail=f"Longitud inválida para el campo {field}, debe tener entre {min_length} y {max_length} caracteres")

    @staticmethod
    def error_email_already_exists() -> HTTPException:
        return HTTPException(status_code=400, detail="El email ya existe")

    @staticmethod
    def error_identification_already_exists() -> HTTPException:
        return HTTPException(status_code=400, detail="El número y tipo de identificación ya existe")

    @staticmethod
    def error_user_not_updated() -> HTTPException:
        return HTTPException(status_code=400, detail="Usuario no actualizado")

    @staticmethod
    def error_user_not_deleted() -> HTTPException:
        return HTTPException(status_code=400, detail="Usuario no eliminado")