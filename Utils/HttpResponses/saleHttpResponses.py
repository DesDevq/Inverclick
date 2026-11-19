from fastapi import HTTPException
from fastapi.responses import JSONResponse
from Utils.HttpResponses.http_response import success_response
from Models.sale import SaleDTO


class SaleHttpResponses:
    @staticmethod
    def success_created(sale: SaleDTO) -> JSONResponse:
        return success_response(sale, "Venta registrada exitosamente", 201)

    @staticmethod
    def success_get(sale: SaleDTO) -> JSONResponse:
        return success_response(sale, "Venta obtenida exitosamente", 200)

    @staticmethod
    def success_get_all(sales: list[SaleDTO]) -> JSONResponse:
        return success_response(sales, "Ventas obtenidas exitosamente", 200)

    @staticmethod
    def error_sale_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="Venta no encontrada")

    @staticmethod
    def error_lead_not_found() -> HTTPException:
        return HTTPException(
            status_code=404, detail="El lead indicado no existe")

    @staticmethod
    def error_property_not_found() -> HTTPException:
        return HTTPException(
            status_code=404, detail="La propiedad indicada no existe")

    # --- Reglas de negocio del CA3 ---

    @staticmethod
    def error_property_already_sold() -> HTTPException:
        return HTTPException(
            status_code=400,
            detail="Esta propiedad ya fue vendida, no se puede vender de nuevo"
        )

    @staticmethod
    def error_property_not_listed() -> HTTPException:
        return HTTPException(
            status_code=400,
            detail="Esta propiedad no está listada en el catálogo disponible, no se puede vender"
        )
