import asyncpg

from ..dto.user_dto import UserDto
from ..entity.user import User


class UserMapper(object):

    @staticmethod
    def user_entity_to_dto(user: User) -> UserDto:
        return UserDto(
            uuid=user.uuid,
            name=user.name,
            email=user.email,
        )

    @staticmethod
    def user_record_to_dto(record: asyncpg.Record) -> UserDto:
        return UserDto(
            uuid=record["uuid"],
            name=record["name"],
            email=record["email"]
        )
