from sqlalchemy.future import select

from ...context.context_local import CONNECTION_HANDLER_CTX
from ...database.asyncpg_pool import AsyncPGPool
from ...database.session import Session
from ...dto.user_dto import UserDto
from ...entity.user import User
from ...enum.connection_type_enum import ConnectionTypeEnum
from ...mapper.user_mapper import UserMapper
from ...statement.user_statement import UserStatement
from ..user_repository import UserRepository


class UserRepositoryImpl(UserRepository):
    async def all(self) -> list[UserDto]:
        conn: AsyncPGPool = await CONNECTION_HANDLER_CTX.get_connection("ANALYTICS", ConnectionTypeEnum.ASYNCPG)
        query = UserStatement.get_users(limit=10)
        records = await conn.execute_single_query(query)
        users_dto: list[UserDto] = [UserMapper.user_record_to_dto(record) for record in records]
        return users_dto

    async def find_by_email(self, email: str) -> UserDto:
        session: Session = await CONNECTION_HANDLER_CTX.get_connection("ANALYTICS", ConnectionTypeEnum.SESSION)
        async with session.session() as async_session:
            query = select(User).where(User.email == email).limit(1)
            result = await async_session.execute(query)
            data: User = result.scalars().one()
            user_dto: UserDto = UserMapper.user_entity_to_dto(data)
            return user_dto
