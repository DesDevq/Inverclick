from Repositories.ILogRepository import ILogRepository
from Models.log import LogDTO


class LogService:
    def __init__(self, repository: ILogRepository):
        self.repository = repository

    def create(self, log: LogDTO) -> LogDTO:
        return self.repository.create(log)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[LogDTO]:
        return self.repository.get_all(skip, limit)
