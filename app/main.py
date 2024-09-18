from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from .api.api import router
from .api.context.context_local import CONNECTION_HANDLER_CTX
from .api.database.asyncpg_pool import AsyncPGPool
from .api.database.session import Session
from .api.enum.connection_type_enum import ConnectionTypeEnum
from .api.property.config_properties import config_properties


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=config_properties.APP_NAME,
        version="0.0.1",
        description="Description",
        routes=app.routes,
        servers=app.servers
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://tecnasic.aimacloud.app/assets/aima_logos/Logotipo-AIMA---negro.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@asynccontextmanager
async def lifespan(_app: FastAPI):
    try:
        print("Starting Application")

        _app.openapi = custom_openapi

        if config_properties.ANALYTICS_DB_HOST is not None:
            try:
                analytics_session = Session(config_properties.session_url_analytics)
                analytics_asyncpg = AsyncPGPool(config_properties.asyncpg_url_analytics)
                await CONNECTION_HANDLER_CTX.add_connection("ANALYTICS", ConnectionTypeEnum.SESSION,
                                                            analytics_session)
                await CONNECTION_HANDLER_CTX.add_connection("ANALYTICS", ConnectionTypeEnum.ASYNCPG,
                                                            analytics_asyncpg)
            except Exception as e:
                print("error creating analytics connections on startup:", str(e))
        yield
    finally:
        print("Closing Application")
        await CONNECTION_HANDLER_CTX.remove_all()
        print("Connections removed")


def create_application() -> FastAPI:
    fastapi = FastAPI(
        redoc_url="/api/documentation",
        lifespan=lifespan
    )
    fastapi.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    fastapi.include_router(router)

    return fastapi


app = create_application()
