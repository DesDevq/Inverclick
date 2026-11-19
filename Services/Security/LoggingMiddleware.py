# LoggingMiddleware.py
# CA4: Middleware de auditoría.
#
# A diferencia de AuthMiddleware.py (que es una dependencia que cada
# endpoint debe usar manualmente con Depends), esto es un middleware real
# de FastAPI/Starlette: se registra UNA sola vez en main.py y se ejecuta
# automáticamente en TODAS las peticiones, sin que cada endpoint tenga
# que acordarse de nada.
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from Repositories.database import SessionLocal
from Repositories.LogRepository import LogRepository
from Models.log import LogDTO
from Services.Security.JWTHandler import decode_access_token

# Solo se auditan acciones "críticas" (crear, editar, eliminar).
# Las peticiones de solo lectura (GET) no generan un log.
LOGGED_METHODS = {"POST", "PUT", "PATCH", "DELETE"}

# Cuando ya existan los módulos de Constructoras, Propiedades, Leads y
# Ventas (CA1, CA2 y CA3), se puede limitar la auditoría solo a esas rutas
# agregando aquí sus prefijos y usando el filtro comentado en dispatch().
# Por ahora se deja sin filtrar por ruta, para poder probar el middleware
# ya mismo con los endpoints que sí existen (users, users-role, users-login).
LOGGED_PATH_PREFIXES: tuple[str, ...] = ()


def _get_user_id_from_request(request: Request) -> int | None:
    """Intenta identificar al usuario ejecutor a partir del token JWT
    enviado en el header 'Authorization: Bearer <token>'."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header[len("Bearer "):].strip()
    payload = decode_access_token(token)
    if not payload:
        return None

    user_id = payload.get("sub")
    if user_id is None:
        return None

    try:
        return int(user_id)
    except (TypeError, ValueError):
        return None


class LoggingMiddleware(BaseHTTPMiddleware):
    """Intercepta cada petición HTTP y, si es una acción crítica, guarda
    quién la ejecutó, cuándo, en qué ruta y con qué resultado terminó."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        should_log = request.method in LOGGED_METHODS and (
            not LOGGED_PATH_PREFIXES
            or request.url.path.startswith(LOGGED_PATH_PREFIXES)
        )

        if should_log:
            self._save_log(request, response)

        return response

    def _save_log(self, request: Request, response) -> None:
        db = SessionLocal()
        try:
            user_id = _get_user_id_from_request(request)
            log = LogDTO(
                user_id=user_id,
                http_method=request.method,
                route=request.url.path,
                status_code=response.status_code,
                action_summary=f"{request.method} {request.url.path} -> {response.status_code}",
                created_at=datetime.utcnow(),
            )
            LogRepository(db).create(log)
        except Exception as e:
            # Un fallo al auditar NUNCA debe tumbar la petición real del
            # usuario: solo se registra el error en consola.
            print(f"LOGGING ERROR: No se pudo guardar el log: {e}")
        finally:
            db.close()
