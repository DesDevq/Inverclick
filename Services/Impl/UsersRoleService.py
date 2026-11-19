from typing import Any
from Repositories.IUsersRoleRepository import IUsersRoleRepository
from Models.users_role import UserRoleDTO
from Utils.HttpResponses.userRoleHttpResponses import UserRoleHttpResponses
from Utils.user_role_validator import UserRoleValidator

def validateUserRole(service: "UsersRoleService", roleDTO: UserRoleDTO | dict[str, Any]) -> UserRoleDTO:
    if isinstance(roleDTO, dict):
        role_name = roleDTO.get("role")
        role_dto = UserRoleDTO(**roleDTO)
    else:
        role_name = roleDTO.role
        role_dto = roleDTO

    invalid = service.validator.validate_user_role_dto_lengths(roleDTO)
    if invalid:
        field, min_len, max_len = invalid
        raise service.http_responses.error_invalid_length(field, min_len, max_len)

    if role_name and service.repository.get_by_role(role_name) is not None:
        raise service.http_responses.error_role_already_exists()

    return role_dto

class UsersRoleService:
    def __init__(self, repository: IUsersRoleRepository, http_responses: UserRoleHttpResponses, validator: UserRoleValidator):
        self.repository = repository
        self.http_responses = http_responses
        self.validator = validator

    def get_by_id(self, role_id: int) -> UserRoleDTO | None:
        role: UserRoleDTO | None = self.repository.get_by_id(role_id)
        if role is None:
            raise self.http_responses.error_role_not_found()
        return role

    def get_by_role(self, role_name: str) -> UserRoleDTO | None:
        role: UserRoleDTO | None = self.repository.get_by_role(role_name)
        if role is None:
            raise self.http_responses.error_role_not_found()
        return role

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserRoleDTO]:
        roles: list[UserRoleDTO] = self.repository.get_all(skip, limit)
        return roles

    def create(self, roleDTO: UserRoleDTO) -> UserRoleDTO:
        role_dto = validateUserRole(self, roleDTO)
        role: UserRoleDTO = self.repository.create(role_dto)
        if role is None:
            raise self.http_responses.error_role_not_created()
        return role

    def update(self, role_id: int, role_data: dict[str, Any] | UserRoleDTO) -> UserRoleDTO | None:
        invalid = self.validator.validate_user_role_dto_lengths(role_data)
        if invalid:
            field, min_len, max_len = invalid
            raise self.http_responses.error_invalid_length(field, min_len, max_len)

        role: UserRoleDTO | None = self.repository.update(role_id, role_data)
        if role is None:
            raise self.http_responses.error_role_not_updated()
        return role

    def delete(self, role_id: int) -> bool:
        success: bool = self.repository.delete(role_id)
        if not success:
            raise self.http_responses.error_role_not_deleted()
        return success
