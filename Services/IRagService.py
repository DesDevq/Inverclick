from Models.rag import RagChatRequest, RagChatResponse, RagHealthResponse

#interfaz es solo la que genera la respuesta con la logica de la iomplementacion (impl)
#las interfaces es para no compartir todas las funciones de los servicios

class IRagService:
    def answer(self, request: RagChatRequest) -> RagChatResponse:
        raise NotImplementedError

    def health(self) -> RagHealthResponse:
        raise NotImplementedError