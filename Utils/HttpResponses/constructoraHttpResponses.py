from fastapi import HTTPException
from fastapi.responses import JSONResponse
from Utils.HttpResponses.http_response import success_response
from Models.constructora import ConstructoraDTO

# HTTP responses arma mensajes de error/éxito ya formateados con su código HTTP correspondiente (404, 400, 201, etc.) y un texto explicando qué pasó.
# Un error, si una peticion del usuario salio bien, etc


class ConstructoraHttpResponses:
    @staticmethod
    def success_created(constructoraDTO: ConstructoraDTO) -> JSONResponse:
        return success_response(constructoraDTO, "Constructora creada exitosamente", 201)

    @staticmethod
    def success_get(constructoraDTO: ConstructoraDTO) -> JSONResponse:
        return success_response(constructoraDTO, "Constructora obtenida exitosamente", 200)

    @staticmethod
    def success_get_all(constructoras: list[ConstructoraDTO]) -> JSONResponse:
        return success_response(constructoras, "Constructoras obtenidas exitosamente", 200)

    @staticmethod
    def success_updated(constructoraDTO: ConstructoraDTO) -> JSONResponse:
        return success_response(constructoraDTO, "Constructora actualizada exitosamente", 200)

    @staticmethod
    def success_deleted() -> JSONResponse:
        return success_response(None, "Constructora eliminada exitosamente", 200)

    @staticmethod
    def error_constructora_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="Constructora no encontrada")

    @staticmethod
    def error_constructora_not_created() -> HTTPException:
        return HTTPException(status_code=400, detail="Constructora no creada")

    @staticmethod
    def error_constructora_not_updated() -> HTTPException:
        return HTTPException(status_code=400, detail="Constructora no actualizada")

    @staticmethod
    def error_constructora_not_deleted() -> HTTPException:
        return HTTPException(status_code=400, detail="Constructora no eliminada")

    @staticmethod
    def error_nit_already_exists() -> HTTPException:
        return HTTPException(status_code=400, detail="El NIT ya existe")

    @staticmethod
    def error_invalid_length(field: str, min_length: int, max_length: int) -> HTTPException:
        return HTTPException(status_code=400, detail=f"Longitud inválida para el campo {field}, debe tener entre {min_length} y {max_length} caracteres")

    @staticmethod
    def error_country_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="País no encontrado")
