from typing import Annotated

from fastapi import Header

from ..context.context_local import CONNECTION_HANDLER_CTX
from ..database.asyncpg_pool import AsyncPGPool
from ..database.session import Session
from ..enum.connection_type_enum import ConnectionTypeEnum
from ..property.config_properties import config_properties


class ConnectionDepend(object):

    @staticmethod
    async def create_connection(x_worker_site: Annotated[str, Header(description="The ot database to connect")]):
        identifier: str = x_worker_site.upper()
        if await CONNECTION_HANDLER_CTX.get_connection(identifier, ConnectionTypeEnum.SESSION) is None:
            print(f"CREATING CONNECTION FOR {identifier}... (SESSION)")
            session = Session(
                config_properties.asyncpg_session_url_worker_builder(x_worker_site, ConnectionTypeEnum.SESSION)
            )
            await CONNECTION_HANDLER_CTX.add_connection(identifier, ConnectionTypeEnum.SESSION,
                                                        session)

        if await CONNECTION_HANDLER_CTX.get_connection(identifier, ConnectionTypeEnum.ASYNCPG) is None:
            print(f"CREATING CONNECTION FOR {identifier}... (ASYNCPG)")

            asyncpg = AsyncPGPool(
                config_properties.asyncpg_session_url_worker_builder(x_worker_site, ConnectionTypeEnum.ASYNCPG)
            )

            await CONNECTION_HANDLER_CTX.add_connection(identifier, ConnectionTypeEnum.ASYNCPG,
                                                        asyncpg)
        return x_worker_site
