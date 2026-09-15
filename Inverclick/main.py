from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Repositories.database import verify_db_connection_and_schema
from Controllers.UsersController import router as users_router
from Controllers.Prefixcontroller import router as prefix_router
from Controllers.UsersRoleController import router as users_role_router
from Controllers.UsersLoginController import router as users_login_router
from Controllers.LogsController import router as logs_router
from Controllers.LeadsController import router as leads_router
from Controllers.SalesController import router as sales_router
from Controllers.PropertyPlaceholderController import router as property_placeholder_router
from Services.Security.LoggingMiddleware import LoggingMiddleware

# Verificar la conexión y estructura de la base de datos al arrancar
verify_db_connection_and_schema()

app = FastAPI(
    title="Inverclick API",
    description="API para el semillero de investigación Inverclick",
    version="1.0.0",
)

# Configurar CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modificar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CA4: middleware de auditoría. Se ejecuta en cada petición automáticamente.
app.add_middleware(LoggingMiddleware)

# Registrar los routers
app.include_router(users_router)
app.include_router(prefix_router)
app.include_router(users_role_router)
app.include_router(users_login_router)
app.include_router(logs_router)
app.include_router(leads_router)
app.include_router(sales_router)
app.include_router(property_placeholder_router)
