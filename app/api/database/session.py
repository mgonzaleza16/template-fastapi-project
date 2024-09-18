import contextlib
from typing import AsyncIterator

from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from ..property.config_properties import config_properties


class Session:
    def __init__(self, dsn: PostgresDsn | str):

        self._engine: AsyncEngine | None \
            = create_async_engine(dsn if isinstance(dsn, str) else dsn.unicode_string(),
                                  connect_args={
                                      "server_settings": {
                                          "application_name": config_properties.APP_NAME,
                                          "client_encoding": "utf8"
                                      },

                                  },
                                  pool_pre_ping=True,
                                  )
        self._sessionmaker: async_sessionmaker | None = async_sessionmaker(autocommit=False, bind=self._engine)

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("Session is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
