from sqlalchemy import select
from sqlalchemy.orm import Session
from Models.document import DocumentDTO
from Models.users import UserDTO


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, document_id: int) -> DocumentDTO | None:
        """Obtiene un documento por su ID."""
        statement = select(DocumentDTO).where(DocumentDTO.id == document_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_all_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> list[DocumentDTO]:
        """Obtiene una lista paginada de los documentos de un usuario."""
        statement = (
            select(DocumentDTO)
            .where(DocumentDTO.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(statement).scalars().all())

    def create(self, documentDTO: DocumentDTO) -> DocumentDTO:
        """Crea y persiste un nuevo documento en la base de datos."""
        self.db.add(documentDTO)
        self.db.commit()
        self.db.refresh(documentDTO)
        return documentDTO

    def set_user_document(self, user_id: int, document_id: int) -> None:
        """Asocia el documento como el document_id vigente del usuario."""
        statement = select(UserDTO).where(UserDTO.id == user_id)
        user = self.db.execute(statement).scalar_one_or_none()
        if user is not None:
            user.document_id = document_id
            self.db.commit()
