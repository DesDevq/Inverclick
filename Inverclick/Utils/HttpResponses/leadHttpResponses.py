from fastapi import HTTPException
from fastapi.responses import JSONResponse
from Utils.HttpResponses.http_response import success_response
from Models.lead import LeadDTO


class LeadHttpResponses:
    @staticmethod
    def success_created(lead: LeadDTO) -> JSONResponse:
        return success_response(lead, "Lead creado exitosamente", 201)

    @staticmethod
    def success_get(lead: LeadDTO) -> JSONResponse:
        return success_response(lead, "Lead obtenido exitosamente", 200)

    @staticmethod
    def success_get_all(leads: list[LeadDTO]) -> JSONResponse:
        return success_response(leads, "Leads obtenidos exitosamente", 200)

    @staticmethod
    def success_updated(lead: LeadDTO) -> JSONResponse:
        return success_response(lead, "Lead actualizado exitosamente", 200)

    @staticmethod
    def error_lead_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="Lead no encontrado")

    @staticmethod
    def error_lead_not_created() -> HTTPException:
        return HTTPException(status_code=400, detail="Lead no creado")

    @staticmethod
    def error_lead_not_updated() -> HTTPException:
        return HTTPException(status_code=400, detail="Lead no actualizado")
