import pytest
from loguru import logger

from app.api.context.context_local import CONNECTION_HANDLER_CTX
from app.api.enum.connection_type_enum import ConnectionTypeEnum


@pytest.mark.asyncio
async def test_session_connection():
    """
    Test Analytics connection
    """
    logger.info("Starting test: test_connection.")
    logger.debug("Attempting to retrieve ANALYTICS connection (session)...")
    session = await CONNECTION_HANDLER_CTX.get_connection("ANALYTICS", ConnectionTypeEnum.SESSION)

    if session:
        logger.info("ANALYTICS connection successfully retrieved.")
    else:
        logger.error("Failed to retrieve ANALYTICS connection.")

    assert session is not None, "Session should be configured manually."
    logger.info("Finalizing test: test_connection.")


@pytest.mark.asyncio
async def test_asyncpg_connection():
    """
    Test to verify that the ANALYTICS asyncpg connection is correctly retrieved.
    """
    logger.info("Starting test: test_asyncpg_connection.")
    logger.debug("Attempting to retrieve ANALYTICS connection (asyncpg)...")

    connection_pool = await CONNECTION_HANDLER_CTX.get_connection("ANALYTICS", ConnectionTypeEnum.ASYNCPG)

    assert connection_pool is not None, "AsyncPG connection pool should be configured and retrieved successfully."

    if connection_pool:
        logger.info("ANALYTICS asyncpg connection successfully retrieved.")
    else:
        logger.error("Failed to retrieve ANALYTICS asyncpg connection.")

    logger.info("Finalizing test: test_asyncpg_connection.")
