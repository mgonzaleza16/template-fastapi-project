import httpx
import pytest_asyncio
from httpx import ASGITransport

from app.api.context.context_local import CONNECTION_HANDLER_CTX
from app.api.database.asyncpg_pool import AsyncPGPool
from app.api.enum.connection_type_enum import ConnectionTypeEnum
from app.main import app


@pytest_asyncio.fixture(scope="session")
async def async_client():
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_connection_for_tests():
    """
    Fixture to automatically set up both SQLAlchemy and asyncpg connections for the ANALYTICS database before each test function.
    Before each test establishes a database session connection.
    After each test removes the database session connection.
    """
    from app.api.database.session import Session
    from app.api.property.config_properties import config_properties

    analytics_session = Session(config_properties.session_url_analytics)
    await CONNECTION_HANDLER_CTX.add_connection("ANALYTICS", ConnectionTypeEnum.SESSION, analytics_session)

    analytics_pool = AsyncPGPool(config_properties.asyncpg_url_analytics)
    await CONNECTION_HANDLER_CTX.add_connection("ANALYTICS", ConnectionTypeEnum.ASYNCPG, analytics_pool)

    yield

    await CONNECTION_HANDLER_CTX.remove_connection("ANALYTICS", ConnectionTypeEnum.SESSION)
    await CONNECTION_HANDLER_CTX.remove_connection("ANALYTICS", ConnectionTypeEnum.ASYNCPG)
