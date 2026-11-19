from typing import Optional, Tuple, Any

class UserLoginValidator:
    """
    Utilidad para verificar y validar las longitudes de los campos del objeto UserLoginDTO o diccionario.
    """

    # Definición de restricciones de longitud por campo: (min_length, max_length)
    # user_password permite contraseñas en texto plano de hasta 100 caracteres.
    FIELD_LENGTHS: dict[str, tuple[int, int]] = {
        "user_login": (1, 100),
        "user_password": (1, 100),
    }

    @classmethod
    def validate_user_login_dto_lengths(cls, login_obj: Any) -> Optional[Tuple[str, int, int]]:
        """
        Valida las longitudes de todos los campos de texto presentes en un objeto UserLoginDTO o dict.

        :param login_obj: Instancia de UserLoginDTO o diccionario a validar.
        :return: None si todos los campos son válidos; de lo contrario, tupla (campo, min_len, max_len).
        """
        for field, (min_len, max_len) in cls.FIELD_LENGTHS.items():
            if isinstance(login_obj, dict):
                value = login_obj.get(field)
            else:
                value = getattr(login_obj, field, None)

            if value is not None:
                val_str = str(value)
                val_len = len(val_str)
                if val_len < min_len or val_len > max_len:
                    return field, min_len, max_len
        return None

    @classmethod
    def validate_field_length(cls, field_name: str, value: Any) -> Optional[Tuple[str, int, int]]:
        """
        Valida la longitud de un campo específico.

        :param field_name: Nombre del campo.
        :param value: Valor del campo.
        :return: None si la longitud es válida; de lo contrario, tupla (campo, min_len, max_len).
        """
        if field_name in cls.FIELD_LENGTHS and value is not None:
            min_len, max_len = cls.FIELD_LENGTHS[field_name]
            val_str = str(value)
            val_len = len(val_str)
            if val_len < min_len or val_len > max_len:
                return field_name, min_len, max_len
        return None
