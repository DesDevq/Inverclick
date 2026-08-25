from typing import Any
from Repositories.IUsuariosRepository import IUsuariosRepository
from Models.users import UserDTO
from Repositories.IPrefixRepository import IPrefixRepository
from Utils.HttpResponses.userHttpResponses import UserHttpResponses
from Utils.user_validator import UserValidator


def validateUser(self, userDTO: UserDTO) -> UserDTO:
    if isinstance(userDTO, dict):
        email = userDTO.get("email")
        identification = userDTO.get("identification")
        identification_type = userDTO.get("identification_type")
        country_id = userDTO.get("country_id")
        user_id_role = userDTO.get("user_id_role")
        user_dto = UserDTO(**userDTO)
    else:
        email = userDTO.email
        identification = userDTO.identification
        identification_type = userDTO.identification_type
        country_id = userDTO.country_id
        user_id_role = getattr(userDTO, "user_id_role", None)
        user_dto = userDTO

    invalid = self.validator.validate_user_dto_lengths(userDTO)
    if invalid:
        field, min_len, max_len = invalid
        raise self.http_responses.error_invalid_length(field, min_len, max_len)

    if country_id:
        country = self.prefix_repository.get_by_id(country_id)
        if country is None:
            raise self.http_responses.error_country_not_found()

    if email and self.repository.get_by_email(email) is not None:
        raise self.http_responses.error_email_already_exists()

    if identification and self.repository.get_by_identification(identification, identification_type) is not None:
        raise self.http_responses.error_identification_already_exists()
    
    return user_dto

class UsuariosService:
    def __init__(self, repository: IUsuariosRepository, prefix_repository: IPrefixRepository, http_responses: UserHttpResponses, validator: UserValidator):
        self.repository = repository
        self.prefix_repository = prefix_repository
        self.http_responses = http_responses
        self.validator = validator

    def get_by_id(self, user_id: int) -> UserDTO | None:
        user: UserDTO | None = self.repository.get_by_id(user_id)
        if user is None:
            raise self.http_responses.error_user_not_found()
        return user

    def get_by_email(self, email: str) -> UserDTO | None:
        user: UserDTO | None = self.repository.get_by_email(email)
        if user is None:
            raise self.http_responses.error_user_not_found()
        return user

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserDTO]:
        users: list[UserDTO] = self.repository.get_all(skip, limit)
        return users

    def create(self, userDTO: UserDTO) -> UserDTO:
        user_dto = validateUser(self, userDTO)
        user: UserDTO = self.repository.create(user_dto)
        if user is None:
            raise self.http_responses.error_user_not_created()
        return user

    def update(self, user_id: int, user_data: dict[str, Any] | UserDTO) -> UserDTO | None:
        invalid = self.validator.validate_user_dto_lengths(user_data)
        if invalid:
            field, min_len, max_len = invalid
            raise self.http_responses.error_invalid_length(field, min_len, max_len)

        user: UserDTO | None = self.repository.update(user_id, user_data)
        if user is None:
            raise self.http_responses.error_user_not_updated()
        return user

    def delete(self, user_id: int) -> bool:
        success: bool = self.repository.delete(user_id)
        if not success:
            raise self.http_responses.error_user_not_deleted()
        return success
