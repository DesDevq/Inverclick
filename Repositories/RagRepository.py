from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from Models.rag import RagChunkDTO

#orm forma sencilla de modelar la base de datos a nivel de codigo
#se crea el modelo de la tabla con los atributos, despues se le crea el repositorio donde se guardan todas las consultas como el select
#para evitar usar codigo sql se puede hacer las consultas y modificaciones desdes el codigo se llama orm, se utiliza para base de datos relacionales

class RagRepository:
    def __init__(self, db: Session):
        self.db = db

    def count(self) -> int:
        statement = select(func.count()).select_from(RagChunkDTO)
        return int(self.db.execute(statement).scalar_one())

#eliminar la fuente de un pdf 
    def delete_by_source(self, source: str) -> None:
        self.db.execute(delete(RagChunkDTO).where(RagChunkDTO.source == source))

    def delete_all(self) -> None:
        self.db.execute(delete(RagChunkDTO))
        self.db.commit()

    def replace_source(self, source: str, chunks: list[RagChunkDTO]) -> int:
        """Reemplaza todos los chunks de un PDF de forma idempotente."""
        self.delete_by_source(source)
        self.db.add_all(chunks)
        self.db.commit()
        return len(chunks)

    def search(
        self,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[tuple[RagChunkDTO, float]]:
        """Busca los chunks más parecidos usando distancia coseno de pgvector."""
        distance = RagChunkDTO.embedding.cosine_distance(query_embedding)
        statement = (
            select(RagChunkDTO, (1 - distance).label("score"))
            .order_by(distance)
            .limit(limit)
        )
        rows = self.db.execute(statement).all()
        return [(row[0], float(row[1])) for row in rows]