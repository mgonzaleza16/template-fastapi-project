import asyncpg
import pandas as pd
from asyncpg.exceptions import ConnectionDoesNotExistError, PostgresError
from asyncpg.pool import Pool
from pydantic import PostgresDsn


class AsyncPGPool:

    def __init__(self, dsn: PostgresDsn | str):
        self._pool: Pool | None = None
        self._dsn = dsn

    async def _create_pool(self):
        self._pool = await asyncpg.create_pool(
            dsn=self._dsn if isinstance(self._dsn, str) else self._dsn.unicode_string(),
            min_size=1,
            max_size=20,
            ssl="require"
        )

    async def execute_single_query(self, query: str, params=None):
        if self._pool is None:
            await self._create_pool()
        try:
            async with self._pool.acquire() as connection:
                if connection.is_closed():
                    raise Exception("Connection was closed, retrying...")
                if params:
                    result = await connection.fetch(query, *params)
                else:
                    result = await connection.fetch(query)
            return result
        except ConnectionDoesNotExistError as e:
            print(f"Connection error while executing query: {e}")
            raise
        except PostgresError as e:
            print(f"Postgres error while executing query: {str(e)}")
            raise Exception(f"An error occurred while executing the query: {str(e)}") from e

    async def execute_queries(self, pool: Pool, queries_with_filenames_and_params: list[tuple[str, str, list]]):
        dataframes = {}
        for filename, query, params in queries_with_filenames_and_params:
            result = await self.execute_single_query(pool, query, params)
            if result:
                column_names = result[0].keys()
                dataframe = pd.DataFrame(result, columns=column_names)
            else:
                dataframe = pd.DataFrame()

            dataframes[filename] = dataframe

        return dataframes
