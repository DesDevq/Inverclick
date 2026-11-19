from Models.log import LogDTO


class ILogRepository:
    def create(self, log: LogDTO) -> LogDTO:
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[LogDTO]:
        pass
