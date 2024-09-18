from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from ..enum.connection_type_enum import ConnectionTypeEnum


class ConfigProperties(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    ANALYTICS_DB_HOST: str
    ANALYTICS_DB_PORT: int
    ANALYTICS_DB_DATABASE: str
    ANALYTICS_DB_USERNAME: str
    ANALYTICS_DB_PASSWORD: str
    OT_DB_HOST: str
    OT_DB_PORT: int
    OT_DB_PASSWORD: str
    APP_NAME: str

    @computed_field
    @property
    def session_url_analytics(self) -> PostgresDsn | str:
        try:
            return MultiHostUrl.build(
                scheme="postgresql+asyncpg",
                username=self.ANALYTICS_DB_USERNAME,
                password=self.ANALYTICS_DB_PASSWORD,
                host=self.ANALYTICS_DB_HOST,
                path=self.ANALYTICS_DB_DATABASE,
                port=self.ANALYTICS_DB_PORT,
                query="ssl=require"
            )
        except Exception as e:
            print("Error creating DSN with Pydantic:", str(e))
            print("Re-trying with normal DSN")
            return f"postgresql+asyncpg://{self.ANALYTICS_DB_USERNAME}:{self.ANALYTICS_DB_PASSWORD}@{self.ANALYTICS_DB_HOST}:{self.ANALYTICS_DB_PORT}/{self.ANALYTICS_DB_DATABASE}"

    @computed_field
    @property
    def asyncpg_url_analytics(self) -> PostgresDsn | str:
        try:
            return MultiHostUrl.build(
                scheme="postgres",
                username=self.ANALYTICS_DB_USERNAME,
                password=self.ANALYTICS_DB_PASSWORD,
                host=self.ANALYTICS_DB_HOST,
                path=self.ANALYTICS_DB_DATABASE,
                port=self.ANALYTICS_DB_PORT,
            )
        except Exception as e:
            print("Error creating DSN with Pydantic:", str(e))
            print("Re-trying with normal DSN")
            return f"postgres://{self.ANALYTICS_DB_USERNAME}:{self.ANALYTICS_DB_PASSWORD}@{self.ANALYTICS_DB_HOST}:{self.ANALYTICS_DB_PORT}/{self.ANALYTICS_DB_DATABASE}"

    def asyncpg_session_url_worker_builder(self, ot: str,
                                           type: ConnectionTypeEnum = ConnectionTypeEnum.SESSION) -> PostgresDsn | str:

        ot = ot.lower().strip()
        schema: str = "postgresql+asyncpg" if type == ConnectionTypeEnum.SESSION else "postgresql"
        try:
            return MultiHostUrl.build(
                scheme=schema,
                username=ot,
                password=ot + self.OT_DB_PASSWORD,
                host=self.OT_DB_HOST,
                path=ot,
                port=self.OT_DB_PORT,
                query="ssl=require"
            )
        except Exception as e:
            print("Error creating DSN with Pydantic:", str(e))
            print("Re-trying with normal DSN")
            return f"{schema}://{ot}:{ot + self.OT_DB_PASSWORD}@{self.OT_DB_HOST}:{self.OT_DB_PORT}/{self.ot}"


config_properties = ConfigProperties()
