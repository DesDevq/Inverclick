from typing import Optional, Tuple, Any


class RealStateValidator:
    """
    Utilidad para verificar y validar las longitudes de los campos del objeto RealStateDTO o diccionario.
    """

    FIELD_LENGTHS: dict[str, tuple[int, int]] = {
        "name": (1, 150),
        "address": (1, 200),
        "description": (1, 500),
        "city": (1, 100),
        "status": (1, 50),
    }

    @classmethod
    def validate_real_state_dto_lengths(cls, real_state_obj: Any) -> Optional[Tuple[str, int, int]]:
        for field, (min_len, max_len) in cls.FIELD_LENGTHS.items():
            if isinstance(real_state_obj, dict):
                value = real_state_obj.get(field)
            else:
                value = getattr(real_state_obj, field, None)

            if value is not None:
                val_str = value.value if hasattr(
                    value, "value") else str(value)
                val_len = len(val_str)
                if val_len < min_len or val_len > max_len:
                    return field, min_len, max_len
        return None
