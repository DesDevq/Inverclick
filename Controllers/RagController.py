#aqui se crean los endpoints

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Models.rag import RagChatRequest, RagChatResponse, RagHealthResponse
from Repositories.RagRepository import RagRepository
from Repositories.database import get_db_session
from Services.IRagService import IRagService
from Services.Impl.RagService import RagService

router = APIRouter(prefix="/rag", tags=["RAG"])


def get_rag_service(db: Session = Depends(get_db_session)) -> IRagService:
    return RagService(repository=RagRepository(db))


@router.post("/chat", response_model=RagChatResponse)
def chat(
    request: RagChatRequest,
    service: IRagService = Depends(get_rag_service),
):
    """Responde preguntas usando los PDFs indexados en Supabase.

    Endpoint público para la demo de clase. En producción debería protegerse
    con el mismo esquema JWT/Keycloak del resto de la API.
    """
    return service.answer(request)

#para saber los estados de los endpointslos estados antes de consumirlos, para saber si esta caido etc
@router.get("/health", response_model=RagHealthResponse)
def health(service: IRagService = Depends(get_rag_service)):
    """Verifica base de datos, modelo de embeddings y configuración del chat."""
    return service.health()