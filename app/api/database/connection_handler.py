from typing import Final

from ..enum.connection_type_enum import ConnectionTypeEnum
from ..schema.connection_schema import ConnectionSchema
from .asyncpg_pool import AsyncPGPool
from .session import Session


class ConnectionHandler:
    _connections: Final[list[ConnectionSchema]] = []

    @property
    def connections(self):
        return self._connections

    async def add_connection(self, id: str, type: ConnectionTypeEnum, connection: Session | AsyncPGPool) -> None:
        self._connections.append(
            ConnectionSchema(connection=connection, identifier=id, type=type)
        )

    async def remove_all(self) -> None:
        for connection in self._connections:
            await self.remove_connection(connection.identifier, connection.type)

    async def remove_connection(self, id: str, type: ConnectionTypeEnum) -> None:
        connection: ConnectionSchema = await self._find_connection(id, type)
        if connection is not None:
            self._connections.remove(connection)

    async def get_connection(self, id: str, type: ConnectionTypeEnum) -> Session | AsyncPGPool | None:
        connection: ConnectionSchema = await self._find_connection(id, type)
        return connection.connection if connection is not None else None

    async def _find_connection(self, id: str, type: ConnectionTypeEnum) -> ConnectionSchema | None:
        for connection in self._connections:
            if connection.identifier == id and connection.type == type:
                return connection
        return None


connection_handler = ConnectionHandler()
