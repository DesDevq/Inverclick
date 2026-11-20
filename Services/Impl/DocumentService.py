import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

from Models.document import DocumentDTO
from Repositories.DocumentRepository import DocumentRepository
from Services.IDocumentService import IDocumentService
from Utils.document_config import settings
from Utils.HttpResponses.documentHttpResponses import DocumentHttpResponses

# Roles internos: pueden subir y consultar PDF, imágenes y hojas de cálculo.
INTERNAL_ROLES = {"admin", "master", "soporte", "constructora"}

# Extensión -> content-type esperado. El rol "Usuario" (cliente) sólo puede usar PDF.
ALLOWED_EXTENSIONS_INTERNAL: dict[str, str] = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".csv": "text/csv",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}

ALLOWED_EXTENSIONS_CLIENT: dict[str, str] = {
    ".pdf": "application/pdf",
}

# Algunos navegadores/sistemas envían content-types alternativos para el mismo formato.
EQUIVALENT_CONTENT_TYPES: dict[str, set[str]] = {
    ".pdf": {"application/pdf"},
    ".png": {"image/png"},
    ".jpg": {"image/jpeg"},
    ".jpeg": {"image/jpeg"},
    ".csv": {"text/csv", "application/vnd.ms-excel", "text/plain"},
    ".xlsx": {
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/octet-stream",
    },
}


class DocumentService(IDocumentService):
    def __init__(self, repository: DocumentRepository, http_responses: DocumentHttpResponses):
        self.repository = repository
        self.http_responses = http_responses

    @staticmethod
    def _allowed_extensions_for_role(role: str | None) -> dict[str, str]:
        if role in INTERNAL_ROLES:
            return ALLOWED_EXTENSIONS_INTERNAL
        return ALLOWED_EXTENSIONS_CLIENT

    def _validate_file(self, file: UploadFile, role: str | None) -> str:
        if file is None:
            raise self.http_responses.error_file_missing()
        if not file.filename:
            raise self.http_responses.error_file_without_name()

        allowed = self._allowed_extensions_for_role(role)
        extension = Path(file.filename).suffix.lower()

        if extension not in allowed:
            raise self.http_responses.error_file_type_not_allowed(sorted(allowed.keys()))

        content_type = (file.content_type or "").lower()
        valid_content_types = EQUIVALENT_CONTENT_TYPES.get(extension, {allowed[extension]})
        if content_type not in valid_content_types:
            raise self.http_responses.error_file_type_not_allowed(sorted(allowed.keys()))

        return extension

    def upload_document(self, file: UploadFile, current_user: dict) -> DocumentDTO:
        role = current_user.get("role")
        user_id = int(current_user.get("user_id"))

        extension = self._validate_file(file, role)

        # Nombre único en disco; nunca se usa el nombre original como ruta
        # (evita colisiones y path traversal).
        stored_filename = f"{uuid.uuid4().hex}{extension}"
        destination = settings.upload_dir / stored_filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        document = DocumentDTO(
            user_id=user_id,
            name=file.filename,
            type=file.content_type or "application/octet-stream",
            location=str(destination),
        )

        created = self.repository.create(document)
        if created is None:
            raise self.http_responses.error_document_not_created()

        self.repository.set_user_document(user_id, created.id)
        return created

    def get_documents(self, current_user: dict, skip: int = 0, limit: int = 100) -> list[DocumentDTO]:
        user_id = int(current_user.get("user_id"))
        return self.repository.get_all_by_user_id(user_id, skip, limit)

    def get_document_file(self, document_id: int, current_user: dict) -> tuple[DocumentDTO, Path]:
        document = self.repository.get_by_id(document_id)
        if document is None:
            raise self.http_responses.error_document_not_found()

        role = current_user.get("role")
        user_id = int(current_user.get("user_id"))

        # Un cliente sólo puede ver sus propios documentos; los roles internos ven cualquiera.
        if role not in INTERNAL_ROLES and document.user_id != user_id:
            raise self.http_responses.error_forbidden_access()

        path = Path(document.location)
        if not path.exists():
            raise self.http_responses.error_document_not_found()

        return document, path
