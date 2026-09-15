from Models.log import LogDTO
from Services.Impl.LogService import LogService


class ILogService:
    """
    Interfaz para el servicio de logs (auditoría).
    """

    def create(self, log: LogDTO) -> LogDTO:
        """Guarda un nuevo registro de auditoría."""
        return LogService.create(self, log)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[LogDTO]:
        """Obtiene una lista paginada de logs, más recientes primero."""
        return LogService.get_all(self, skip, limit)
