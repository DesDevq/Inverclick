# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Obtener la URL (Asegúrate de que no devuelva None)
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el engine. echo=True imprimirá las consultas SQL en la consola (útil en desarrollo)
engine = create_engine(DATABASE_URL, echo=True)

# Configurar la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para definir nuestros modelos (Sintaxis SQLAlchemy 2.0)
class Base(DeclarativeBase):
    pass

# Dependencia para inyectar la sesión en tus rutas o servicios
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para verificar la conexión y la estructura de las tablas sin alterarlas
def verify_db_connection_and_schema():
    from sqlalchemy import inspect, text
    from Models.users import Usuario  # Importación diferida para evitar ciclos
    
    try:
        # 1. Verificar la conexión básica ejecutando una consulta rápida
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("DATABASE: Conexión establecida con éxito.")
            
            # 2. Inspeccionar la base de datos
            inspector = inspect(engine)
            table_name = Usuario.__tablename__
            
            # Verificar si la tabla existe
            if not inspector.has_table(table_name):
                print(f"DATABASE ERROR: La tabla '{table_name}' no existe en la base de datos.")
                return False
                
            # 3. Verificar que las columnas coincidan
            db_columns = {col["name"]: col for col in inspector.get_columns(table_name)}
            model_columns = Usuario.__table__.columns
            
            for col in model_columns:
                if col.name not in db_columns:
                    print(f"DATABASE ERROR: La columna '{col.name}' definida en el modelo no existe en la tabla real.")
                    return False
            
            print(f"DATABASE: Estructura de la tabla '{table_name}' verificada y correcta.")
            return True
            
    except Exception as e:
        print(f"DATABASE ERROR: Fallo al verificar la conexión o estructura: {e}")
        return False
