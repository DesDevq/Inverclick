from typing import Any
from fastapi import HTTPException
from Repositories.ConstructoraRepository import ConstructoraRepository
from Repositories.IPrefixRepository import IPrefixRepository
from Models.constructora import ConstructoraDTO
from Utils.HttpResponses.constructoraHttpResponses import ConstructoraHttpResponses
from Utils.constructora_validator import ConstructoraValidator


def validateConstructora(self, constructoraDTO: ConstructoraDTO) -> ConstructoraDTO:
    if isinstance(constructoraDTO, dict):
        nit = constructoraDTO.get("nit")
        country_id = constructoraDTO.get("country_id")
        constructora_dto = ConstructoraDTO(**constructoraDTO)
    else:
        nit = constructoraDTO.nit
        country_id = constructoraDTO.country_id
        constructora_dto = constructoraDTO

    invalid = self.validator.validate_constructora_dto_lengths(constructoraDTO)
    if invalid:
        field, min_len, max_len = invalid
        raise self.http_responses.error_invalid_length(field, min_len, max_len)

    if country_id:
        country = self.prefix_repository.get_by_id(country_id)
        if country is None:
            raise self.http_responses.error_country_not_found()

    if nit and self.repository.get_by_nit(nit) is not None:
        raise self.http_responses.error_nit_already_exists()

    return constructora_dto


def check_ownership(current_user: dict, constructora_id: int):
    """Si el usuario tiene rol 'constructora', solo puede operar sobre la suya propia."""
    if current_user.get("role") == "constructora":
        if current_user.get("constructora_id") != constructora_id:
            raise HTTPException(
                status_code=403,
                detail="No tiene permiso para acceder o modificar información de otra constructora"
            )


def block_if_constructora(current_user: dict):
    """Bloquea por completo la acción si el rol es 'constructora' (usado en create/delete)."""
    if current_user.get("role") == "constructora":
        raise HTTPException(
            status_code=403,
            detail="No tiene permiso para realizar esta acción"
        )


class ConstructoraService:
    def __init__(
        self,
        repository: ConstructoraRepository,
        prefix_repository: IPrefixRepository,
        http_responses: ConstructoraHttpResponses,
        validator: ConstructoraValidator,
    ):
        self.repository = repository
        self.prefix_repository = prefix_repository
        self.http_responses = http_responses
        self.validator = validator

    def get_by_id(self, constructora_id: int, current_user: dict) -> ConstructoraDTO | None:
        check_ownership(current_user, constructora_id)

        constructora: ConstructoraDTO | None = self.repository.get_by_id(
            constructora_id)
        if constructora is None:
            raise self.http_responses.error_constructora_not_found()
        return constructora

    def get_by_nit(self, nit: str, current_user: dict) -> ConstructoraDTO | None:
        constructora: ConstructoraDTO | None = self.repository.get_by_nit(nit)
        if constructora is None:
            raise self.http_responses.error_constructora_not_found()

        check_ownership(current_user, constructora.id)
        return constructora

    def get_all(self, current_user: dict, skip: int = 0, limit: int = 100) -> list[ConstructoraDTO]:
        if current_user.get("role") == "constructora":
            constructora_id = current_user.get("constructora_id")
            propia = self.repository.get_by_id(
                constructora_id) if constructora_id else None
            return [propia] if propia else []

        constructoras: list[ConstructoraDTO] = self.repository.get_all(
            skip, limit)
        return constructoras

    def create(self, constructoraDTO: ConstructoraDTO, current_user: dict) -> ConstructoraDTO:
        block_if_constructora(current_user)

        constructora_dto = validateConstructora(self, constructoraDTO)
        constructora: ConstructoraDTO = self.repository.create(
            constructora_dto)
        if constructora is None:
            raise self.http_responses.error_constructora_not_created()
        return constructora

    def update(self, constructora_id: int, constructora_data: dict[str, Any] | ConstructoraDTO, current_user: dict) -> ConstructoraDTO | None:
        check_ownership(current_user, constructora_id)

        invalid = self.validator.validate_constructora_dto_lengths(
            constructora_data)
        if invalid:
            field, min_len, max_len = invalid
            raise self.http_responses.error_invalid_length(
                field, min_len, max_len)

        constructora: ConstructoraDTO | None = self.repository.update(
            constructora_id, constructora_data)
        if constructora is None:
            raise self.http_responses.error_constructora_not_updated()
        return constructora

    def delete(self, constructora_id: int, current_user: dict) -> bool:
        block_if_constructora(current_user)

        success: bool = self.repository.delete(constructora_id)
        if not success:
            raise self.http_responses.error_constructora_not_deleted()
        return success
