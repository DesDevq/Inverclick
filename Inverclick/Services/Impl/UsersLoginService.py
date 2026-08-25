from typing import Any
from Repositories.IUsersLoginRepository import IUsersLoginRepository
from Repositories.IUsuariosRepository import IUsuariosRepository
from Models.users_login import UserLoginDTO
from Utils.HttpResponses.userLoginHttpResponses import UserLoginHttpResponses
from Utils.user_login_validator import UserLoginValidator
from Services.Security.CryptPass import get_password_hash, verify_password

def validateUserLogin(service: "UsersLoginService", loginDTO: UserLoginDTO | dict[str, Any]) -> UserLoginDTO:
    if isinstance(loginDTO, dict):
        user_id = loginDTO.get("user_id")
        user_login = loginDTO.get("user_login")
        login_dto = UserLoginDTO(**loginDTO)
    else:
        user_id = loginDTO.user_id
        user_login = loginDTO.user_login
        login_dto = loginDTO

    invalid = service.validator.validate_user_login_dto_lengths(loginDTO)
    if invalid:
        field, min_len, max_len = invalid
        raise service.http_responses.error_invalid_length(field, min_len, max_len)

    if user_id and service.users_repository:
        user = service.users_repository.get_by_id(user_id)
        if user is None:
            raise service.http_responses.error_user_not_found()

    if user_login and service.repository.get_by_user_login(user_login) is not None:
        raise service.http_responses.error_login_already_exists()

    return login_dto

class UsersLoginService:
    def __init__(
        self, 
        repository: IUsersLoginRepository, 
        http_responses: UserLoginHttpResponses, 
        validator: UserLoginValidator,
        users_repository: IUsuariosRepository | None = None
    ):
        self.repository = repository
        self.http_responses = http_responses
        self.validator = validator
        self.users_repository = users_repository

    def get_by_id(self, login_id: int) -> UserLoginDTO | None:
        login: UserLoginDTO | None = self.repository.get_by_id(login_id)
        if login is None:
            raise self.http_responses.error_login_not_found()
        return login

    def get_by_user_id(self, user_id: int) -> UserLoginDTO | None:
        login: UserLoginDTO | None = self.repository.get_by_user_id(user_id)
        if login is None:
            raise self.http_responses.error_login_not_found()
        return login

    def get_by_user_login(self, user_login: str) -> UserLoginDTO | None:
        login: UserLoginDTO | None = self.repository.get_by_user_login(user_login)
        if login is None:
            raise self.http_responses.error_login_not_found()
        return login

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserLoginDTO]:
        logins: list[UserLoginDTO] = self.repository.get_all(skip, limit)
        return logins

    def create(self, loginDTO: UserLoginDTO) -> UserLoginDTO:
        login_dto = validateUserLogin(self, loginDTO)
        # Hashear la contraseña antes de persistir en la base de datos
        if login_dto.user_password:
            login_dto.user_password = get_password_hash(login_dto.user_password)

        login: UserLoginDTO = self.repository.create(login_dto)
        if login is None:
            raise self.http_responses.error_login_not_created()
        return login

    def update(self, login_id: int, login_data: dict[str, Any] | UserLoginDTO) -> UserLoginDTO | None:
        invalid = self.validator.validate_user_login_dto_lengths(login_data)
        if invalid:
            field, min_len, max_len = invalid
            raise self.http_responses.error_invalid_length(field, min_len, max_len)

        # Hashear la nueva contraseña si viene presente en la actualización
        if isinstance(login_data, dict):
            data_to_update = login_data.copy()
            if "user_password" in data_to_update and data_to_update["user_password"]:
                data_to_update["user_password"] = get_password_hash(data_to_update["user_password"])
        else:
            data_to_update = login_data
            if data_to_update.user_password:
                data_to_update.user_password = get_password_hash(data_to_update.user_password)

        login: UserLoginDTO | None = self.repository.update(login_id, data_to_update)
        if login is None:
            raise self.http_responses.error_login_not_updated()
        return login

    def delete(self, login_id: int) -> bool:
        success: bool = self.repository.delete(login_id)
        if not success:
            raise self.http_responses.error_login_not_deleted()
        return success

    def verify_credentials(self, user_login: str, plain_password: str) -> UserLoginDTO | None:
        """Compara la contraseña en texto plano contra el hash almacenado."""
        login = self.repository.get_by_user_login(user_login)
        if login is None or not login.user_password:
            return None
        if not verify_password(plain_password, login.user_password):
            return None
        return login

    def authenticate(self, user_login: str, plain_password: str) -> UserLoginDTO:
        """Autentica las credenciales y el estado activo del usuario."""
        login = self.repository.get_by_user_login(user_login)
        if login is None or not login.user_password:
            raise self.http_responses.error_invalid_credentials()
        if not verify_password(plain_password, login.user_password):
            raise self.http_responses.error_invalid_credentials()
        if not login.active:
            raise self.http_responses.error_account_inactive()
        return login
