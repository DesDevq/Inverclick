from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from Controllers import BanksController, ConstructionCompanyController, ConstructionPhasesController, LeadsController, PropertySoldController, RagController, RealEstateController
from Controllers.AuthController import router as auth_router
from Controllers.Prefixcontroller import router as prefix_router
from Controllers.UsersController import router as users_router
from Controllers.UsersLoginController import router as users_login_router
from Controllers.UsersRoleController import router as users_role_router
from Repositories.database import verify_db_connection_and_schema
from Utils.middlewares import AuditLogMiddleware

verify_db_connection_and_schema()

app = FastAPI(
    title="Inverclick API",
    description="API para el semillero de investigación Inverclick (auth híbrida local + Keycloak)",
    version="2.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuditLogMiddleware)

app.include_router(users_router)
app.include_router(prefix_router)
app.include_router(users_role_router)
app.include_router(users_login_router)
app.include_router(auth_router)
app.include_router(RealEstateController.router)
app.include_router(ConstructionCompanyController.router)
app.include_router(ConstructionPhasesController.router)
app.include_router(PropertySoldController.router)
app.include_router(BanksController.router)
app.include_router(LeadsController.router)
app.include_router(RagController.router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Un solo esquema Authorize en Swagger (HTTPBearer usa scheme_name="BearerAuth")
    schemes = openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})
    schemes.pop("HTTPBearer", None)
    schemes["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "Pega solo el access_token (sin la palabra Bearer).",
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi