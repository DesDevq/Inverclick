from datetime import date, datetime
from typing import Optional, Tuple, Any

class UserValidator:
    """
    Utilidad para verificar y validar las longitudes de los campos del objeto UserDTO o diccionario.
    """

    # Definición de restricciones de longitud por campo: (min_length, max_length)
    FIELD_LENGTHS: dict[str, tuple[int, int]] = {
        "name": (1, 100),
        "last_name": (1, 100),
        "email": (1, 100),
        "identification": (1, 100),
        "identification_type": (1, 3),
        "residence_city": (1, 20),
        "street_address": (1, 100),
        "zip_code": (1, 100),
        "phone_number": (1, 20),
        "job": (1, 100),
        "monthly_income": (1, 100),
        "monthly_outcome": (1, 100),
        "desired_description": (1, 500),
    }

    @classmethod
    def validate_user_dto_lengths(cls, user_obj: Any) -> Optional[Tuple[str, int, int]]:
        """
        Valida las longitudes de todos los campos de texto presentes en un objeto UserDTO o dict.

        :param user_obj: Instancia de UserDTO o diccionario a validar.
        :return: None si todos los campos son válidos; de lo contrario, tupla (campo, min_len, max_len).
        """
        for field, (min_len, max_len) in cls.FIELD_LENGTHS.items():
            if isinstance(user_obj, dict):
                value = user_obj.get(field)
            else:
                value = getattr(user_obj, field, None)

            if value is not None:
                if isinstance(value, (date, datetime)):
                    continue
                val_str = value.value if hasattr(value, "value") else str(value)
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
            if isinstance(value, (date, datetime)):
                return None
            min_len, max_len = cls.FIELD_LENGTHS[field_name]
            val_str = value.value if hasattr(value, "value") else str(value)
            val_len = len(val_str)
            if val_len < min_len or val_len > max_len:
                return field_name, min_len, max_len
        return None
