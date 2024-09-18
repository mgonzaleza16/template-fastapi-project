from pydantic import BaseModel, ConfigDict

from ..database.asyncpg_pool import AsyncPGPool
from ..database.session import Session
from ..enum.connection_type_enum import ConnectionTypeEnum


class ConnectionSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    connection: Session | AsyncPGPool
    identifier: str
    type: ConnectionTypeEnum
