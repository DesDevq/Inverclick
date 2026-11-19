from fastapi import HTTPException
from fastapi.responses import JSONResponse
from Utils.HttpResponses.http_response import success_response
from Models.real_state import RealStateDTO


class RealStateHttpResponses:
    @staticmethod
    def success_created(real_stateDTO: RealStateDTO) -> JSONResponse:
        return success_response(real_stateDTO, "Propiedad creada exitosamente", 201)

    @staticmethod
    def success_get(real_stateDTO: RealStateDTO) -> JSONResponse:
        return success_response(real_stateDTO, "Propiedad obtenida exitosamente", 200)

    @staticmethod
    def success_get_all(real_states: list[RealStateDTO]) -> JSONResponse:
        return success_response(real_states, "Propiedades obtenidas exitosamente", 200)

    @staticmethod
    def success_updated(real_stateDTO: RealStateDTO) -> JSONResponse:
        return success_response(real_stateDTO, "Propiedad actualizada exitosamente", 200)

    @staticmethod
    def success_deleted() -> JSONResponse:
        return success_response(None, "Propiedad eliminada exitosamente", 200)

    @staticmethod
    def error_real_state_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="Propiedad no encontrada")

    @staticmethod
    def error_real_state_not_created() -> HTTPException:
        return HTTPException(status_code=400, detail="Propiedad no creada")

    @staticmethod
    def error_real_state_not_updated() -> HTTPException:
        return HTTPException(status_code=400, detail="Propiedad no actualizada")

    @staticmethod
    def error_real_state_not_deleted() -> HTTPException:
        return HTTPException(status_code=400, detail="Propiedad no eliminada")

    @staticmethod
    def error_name_already_exists() -> HTTPException:
        return HTTPException(status_code=400, detail="Ya existe una propiedad con ese nombre")

    @staticmethod
    def error_address_already_exists() -> HTTPException:
        return HTTPException(status_code=400, detail="Ya existe una propiedad con esa dirección")

    @staticmethod
    def error_constructora_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="Constructora no encontrada")

    @staticmethod
    def error_country_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="País no encontrado")

    @staticmethod
    def error_invalid_length(field: str, min_length: int, max_length: int) -> HTTPException:
        return HTTPException(status_code=400, detail=f"Longitud inválida para el campo {field}, debe tener entre {min_length} y {max_length} caracteres")
