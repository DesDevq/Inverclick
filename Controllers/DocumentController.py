from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from Models.document import DocumentResponseSchema
from Repositories.database import get_db
from Repositories.DocumentRepository import DocumentRepository
from Services.IDocumentService import IDocumentService
from Services.Impl.DocumentService import DocumentService
from Services.Security.AuthMiddleware import get_current_user_context, require_module
from Utils.HttpResponses.documentHttpResponses import DocumentHttpResponses

router = APIRouter(prefix="/documents", tags=["Documents"])


def get_document_service(db: Session = Depends(get_db)) -> IDocumentService:
    repository = DocumentRepository(db)
    http_responses = DocumentHttpResponses()
    return DocumentService(repository, http_responses)


# solo puede acceder el rol que tenga como modulo "documents" (o "All")
@router.post(
    "/upload",
    status_code=201,
    response_model=DocumentResponseSchema,
    dependencies=[Depends(require_module("documents"))],
)
def upload_document(
    file: UploadFile = File(...),
    service: IDocumentService = Depends(get_document_service),
    current_user: dict = Depends(get_current_user_context),
):
    return service.upload_document(file, current_user)


@router.get(
    "",
    response_model=list[DocumentResponseSchema],
    dependencies=[Depends(require_module("documents"))],
)
def get_my_documents(
    skip: int = 0,
    limit: int = 100,
    service: IDocumentService = Depends(get_document_service),
    current_user: dict = Depends(get_current_user_context),
):
    return service.get_documents(current_user, skip=skip, limit=limit)


@router.get(
    "/{document_id}",
    dependencies=[Depends(require_module("documents"))],
)
def download_document(
    document_id: int,
    service: IDocumentService = Depends(get_document_service),
    current_user: dict = Depends(get_current_user_context),
):
    document, path = service.get_document_file(document_id, current_user)
    return FileResponse(path=path, media_type=document.type, filename=document.name)
