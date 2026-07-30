from typing import Any
from fastapi.responses import JSONResponse
from Utils.enums import ResponseStatus

def custom_response(status: ResponseStatus, code: int, message: str, data: Any = None) -> JSONResponse:
    """
    Genera una estructura de respuesta HTTP estandarizada para toda la aplicación.
    """
    content = {
        "status": status.value,
        "code": code,
        "message": message,
        "data": data
    }
    return JSONResponse(status_code=code, content=content)

def success_response(data: Any = None, message: str = "Operación realizada con éxito", code: int = 200) -> JSONResponse:
    """
    Retorna una respuesta de éxito estandarizada.
    """
    return custom_response(ResponseStatus.SUCCESS, code, message, data)

def error_response(message: str = "Ha ocurrido un error", code: int = 400, data: Any = None) -> JSONResponse:
    """
    Retorna una respuesta de error estandarizada.
    """
    return custom_response(ResponseStatus.ERROR, code, message, data)

def warning_response(message: str, code: int = 400, data: Any = None) -> JSONResponse:
    """
    Retorna una respuesta de advertencia estandarizada.
    """
    return custom_response(ResponseStatus.WARNING, code, message, data)

def info_response(message: str, data: Any = None, code: int = 200) -> JSONResponse:
    """
    Retorna una respuesta informativa estandarizada.
    """
    return custom_response(ResponseStatus.INFO, code, message, data)
