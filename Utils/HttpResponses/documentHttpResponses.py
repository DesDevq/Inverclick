from fastapi import HTTPException
from fastapi.responses import JSONResponse
from Utils.HttpResponses.http_response import success_response
from Models.document import DocumentDTO


class DocumentHttpResponses:
    @staticmethod
    def success_created(documentDTO: DocumentDTO) -> JSONResponse:
        return success_response(documentDTO, "Documento subido exitosamente", 201)

    @staticmethod
    def success_get_all(documents: list[DocumentDTO]) -> JSONResponse:
        return success_response(documents, "Documentos obtenidos exitosamente", 200)

    @staticmethod
    def error_document_not_found() -> HTTPException:
        return HTTPException(status_code=404, detail="Documento no encontrado")

    @staticmethod
    def error_document_not_created() -> HTTPException:
        return HTTPException(status_code=400, detail="Documento no creado")

    @staticmethod
    def error_file_missing() -> HTTPException:
        return HTTPException(status_code=400, detail="No se recibió ningún archivo")

    @staticmethod
    def error_file_without_name() -> HTTPException:
        return HTTPException(status_code=400, detail="El archivo no tiene nombre")

    @staticmethod
    def error_file_type_not_allowed(allowed_extensions: list[str]) -> HTTPException:
        return HTTPException(
            status_code=400,
            detail=(
                "Tipo de archivo no permitido para su rol. "
                f"Formatos permitidos: {', '.join(allowed_extensions)}"
            ),
        )

    @staticmethod
    def error_forbidden_access() -> HTTPException:
        return HTTPException(
            status_code=403,
            detail="No tiene permiso para acceder a este documento",
        )
