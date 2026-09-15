from typing import Any
from fastapi import HTTPException
from Repositories.RealStateRepository import RealStateRepository
from Repositories.ConstructoraRepository import ConstructoraRepository
from Repositories.IPrefixRepository import IPrefixRepository
from Models.real_state import RealStateDTO
from Utils.HttpResponses.realStateHttpResponses import RealStateHttpResponses
from Utils.real_state_validator import RealStateValidator


def validateRealState(self, real_stateDTO: RealStateDTO) -> RealStateDTO:
    if isinstance(real_stateDTO, dict):
        name = real_stateDTO.get("name")
        address = real_stateDTO.get("address")
        constructora_id = real_stateDTO.get("constructora_id")
        country_id = real_stateDTO.get("country_id")
        real_state_dto = RealStateDTO(**real_stateDTO)
    else:
        name = real_stateDTO.name
        address = real_stateDTO.address
        constructora_id = real_stateDTO.constructora_id
        country_id = real_stateDTO.country_id
        real_state_dto = real_stateDTO

    # Validación de longitud de campos de texto
    invalid = self.validator.validate_real_state_dto_lengths(real_stateDTO)
    if invalid:
        field, min_len, max_len = invalid
        raise self.http_responses.error_invalid_length(field, min_len, max_len)

    # La constructora asociada debe existir (obligatorio, según CA2)
    if constructora_id:
        constructora = self.constructora_repository.get_by_id(constructora_id)
        if constructora is None:
            raise self.http_responses.error_constructora_not_found()

    # El país debe existir, si se proporciona
    if country_id:
        country = self.prefix_repository.get_by_id(country_id)
        if country is None:
            raise self.http_responses.error_country_not_found()

    # Nombre único en todo el sistema (CA2)
    if name and self.repository.get_by_name(name) is not None:
        raise self.http_responses.error_name_already_exists()

    # Dirección única en todo el sistema (CA2)
    if address and self.repository.get_by_address(address) is not None:
        raise self.http_responses.error_address_already_exists()

    return real_state_dto


def check_ownership(current_user: dict, constructora_id: int):
    """Si el usuario tiene rol 'constructora', solo puede operar sobre propiedades de su propia constructora."""
    if current_user.get("role") == "constructora":
        if current_user.get("constructora_id") != constructora_id:
            raise HTTPException(
                status_code=403,
                detail="No tiene permiso para acceder o modificar propiedades de otra constructora"
            )


class RealStateService:
    def __init__(
        self,
        repository: RealStateRepository,
        constructora_repository: ConstructoraRepository,
        prefix_repository: IPrefixRepository,
        http_responses: RealStateHttpResponses,
        validator: RealStateValidator,
    ):
        self.repository = repository
        self.constructora_repository = constructora_repository
        self.prefix_repository = prefix_repository
        self.http_responses = http_responses
        self.validator = validator

    def get_by_id(self, real_state_id: int, current_user: dict) -> RealStateDTO | None:
        real_state: RealStateDTO | None = self.repository.get_by_id(
            real_state_id)
        if real_state is None:
            raise self.http_responses.error_real_state_not_found()

        check_ownership(current_user, real_state.constructora_id)
        return real_state

    def get_all(self, current_user: dict, skip: int = 0, limit: int = 100) -> list[RealStateDTO]:
        # Si el usuario es de una constructora, solo ve las propiedades de la suya
        if current_user.get("role") == "constructora":
            constructora_id = current_user.get("constructora_id")
            if constructora_id is None:
                return []
            return self.repository.get_by_constructora(constructora_id, skip, limit)

        real_states: list[RealStateDTO] = self.repository.get_all(skip, limit)
        return real_states

    def create(self, real_stateDTO: RealStateDTO, current_user: dict) -> RealStateDTO:
        constructora_id = real_stateDTO.get("constructora_id") if isinstance(
            real_stateDTO, dict) else real_stateDTO.constructora_id
        check_ownership(current_user, constructora_id)

        real_state_dto = validateRealState(self, real_stateDTO)
        real_state: RealStateDTO = self.repository.create(real_state_dto)
        if real_state is None:
            raise self.http_responses.error_real_state_not_created()
        return real_state

    def update(self, real_state_id: int, real_state_data: dict[str, Any] | RealStateDTO, current_user: dict) -> RealStateDTO | None:
        existente = self.repository.get_by_id(real_state_id)
        if existente is None:
            raise self.http_responses.error_real_state_not_found()

        check_ownership(current_user, existente.constructora_id)

        invalid = self.validator.validate_real_state_dto_lengths(
            real_state_data)
        if invalid:
            field, min_len, max_len = invalid
            raise self.http_responses.error_invalid_length(
                field, min_len, max_len)

        real_state: RealStateDTO | None = self.repository.update(
            real_state_id, real_state_data)
        if real_state is None:
            raise self.http_responses.error_real_state_not_updated()
        return real_state

    def delete(self, real_state_id: int, current_user: dict) -> bool:
        existente = self.repository.get_by_id(real_state_id)
        if existente is None:
            raise self.http_responses.error_real_state_not_found()

        check_ownership(current_user, existente.constructora_id)

        success: bool = self.repository.delete(real_state_id)
        if not success:
            raise self.http_responses.error_real_state_not_deleted()
        return success
