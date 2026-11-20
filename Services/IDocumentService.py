from pathlib import Path

from fastapi import UploadFile

from Models.document import DocumentDTO

#interfaz es solo la que genera la respuesta con la logica de la implementacion (impl)
#las interfaces es para no compartir todas las funciones de los servicios


class IDocumentService:
    def upload_document(self, file: UploadFile, current_user: dict) -> DocumentDTO:
        raise NotImplementedError

    def get_documents(self, current_user: dict, skip: int = 0, limit: int = 100) -> list[DocumentDTO]:
        raise NotImplementedError

    def get_document_file(self, document_id: int, current_user: dict) -> tuple[DocumentDTO, Path]:
        raise NotImplementedError
