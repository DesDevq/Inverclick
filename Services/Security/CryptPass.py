import hashlib
import bcrypt

def _prepare_password(password: str) -> bytes:
    """
    Aplica SHA-256 (retorna 32 bytes) para eliminar de raíz la limitación
    de 72 bytes de Bcrypt sin truncar la contraseña original.
    Esto permite soportar contraseñas de hasta 100+ caracteres de forma íntegra.
    """
    return hashlib.sha256(password.encode("utf-8")).digest()

def get_password_hash(password: str) -> str:
    """
    Recibe la contraseña en texto plano y genera un hash Bcrypt seguro (60 caracteres),
    el cual se almacena perfectamente en un campo VARCHAR(255).
    """
    prepared = _prepare_password(password)
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(prepared, salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compara la contraseña en texto plano ingresada contra el hash
    almacenado en la base de datos.
    """
    try:
        prepared = _prepare_password(plain_password)
        return bcrypt.checkpw(prepared, hashed_password.encode("utf-8"))
    except Exception:
        return False
