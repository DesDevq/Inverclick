from typing import Optional, Tuple, Any

# Validator define los rangos permitidos para cada campo de texto, y revisa si algún valor se pasa o queda corto.


class ConstructoraValidator:
    """
    Utilidad para verificar y validar las longitudes de los campos del objeto ConstructoraDTO o diccionario.
    """

    # Definición de restricciones de longitud por campo: (min_length, max_length)
    FIELD_LENGTHS: dict[str, tuple[int, int]] = {
        "name": (1, 150),
        "nit": (1, 50),
        "email": (1, 100),
        "phone": (1, 20),
        "address": (1, 150),
    }

    @classmethod
    def validate_constructora_dto_lengths(cls, constructora_obj: Any) -> Optional[Tuple[str, int, int]]:
        """
        Valida las longitudes de todos los campos de texto presentes en un objeto ConstructoraDTO o dict.

        :param constructora_obj: Instancia de ConstructoraDTO o diccionario a validar.
        :return: None si todos los campos son válidos; de lo contrario, tupla (campo, min_len, max_len).
        """
        for field, (min_len, max_len) in cls.FIELD_LENGTHS.items():
            if isinstance(constructora_obj, dict):
                value = constructora_obj.get(field)
            else:
                value = getattr(constructora_obj, field, None)

            if value is not None:
                val_str = value.value if hasattr(
                    value, "value") else str(value)
                val_len = len(val_str)
                if val_len < min_len or val_len > max_len:
                    return field, min_len, max_len
        return None
