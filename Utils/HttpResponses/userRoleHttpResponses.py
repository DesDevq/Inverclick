from fastapi import HTTPException
from fastapi.responses import JSONResponse
from Utils.HttpResponses.http_response import success_response
from Models.users_role import UserRoleDTO

class UserRoleHttpResponses:
    @staticmethod
    def success_created(roleDTO: UserRoleDTO) -> JSONResponse:
        return success_response(roleDTO, "Rol de usuario creado exitosamente", 201)

    @staticmethod
    def success_get(roleDTO: UserRoleDTO) -> JSONResponse:
        return success_response(roleDTO, "Rol de usuario obtenido exitosamente", 200)

    @staticmethod   
    def success_get_all(roles: list[UserRoleDTO]) -> JSONResponse:
        return success_response(roles, "Roles de usuario obtenidos exitosamente", 200)

    @staticmethod
    def success_updated(roleDTO: UserRoleDTO) -> JSONResponse:
        return success_response(roleDTO, "Rol de usuario actualizado exitosamente", 200)

    @staticmethod
    def success_deleted() -> JSONResponse:
        return success_response(None, "Rol de usuario eliminado exitosamente", 200)

    @staticmethod
    def error_role_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="Rol de usuario no encontrado")

    @staticmethod
    def error_role_already_exists() -> HTTPException:
        return HTTPException(status_code=400, detail="El rol de usuario ya existe")

    @staticmethod
    def error_role_not_created() -> HTTPException:
        return HTTPException(status_code=400, detail="Rol de usuario no creado")

    @staticmethod
    def error_invalid_length(field: str, min_length: int, max_length: int) -> HTTPException:
        return HTTPException(status_code=400, detail=f"Longitud inválida para el campo {field}, debe tener entre {min_length} y {max_length} caracteres")

    @staticmethod
    def error_role_not_updated() -> HTTPException:
        return HTTPException(status_code=400, detail="Rol de usuario no actualizado")

    @staticmethod
    def error_role_not_deleted() -> HTTPException:
        return HTTPException(status_code=400, detail="Rol de usuario no eliminado")
