from sqlalchemy.future import select

from ...context.context_local import CONNECTION_HANDLER_CTX
from ...database.session import Session
from ...entity.chat_bot_activity import ChatBotActivity
from ...enum.connection_type_enum import ConnectionTypeEnum
from ..chat_bot_activity_repository import ChatBotActivityRepository


class ChatBotActivityRepositoryImpl(ChatBotActivityRepository):
    async def all(self, worker: str) -> list:
        session: Session = await CONNECTION_HANDLER_CTX.get_connection(worker.upper(), ConnectionTypeEnum.SESSION)
        async with session.session() as async_session:
            query = select(ChatBotActivity)
            result = await async_session.execute(query)
            data = result.scalars().all()
            return data

    async def find_by_task_code(self, worker: str, task_code: str):
        session: Session = await CONNECTION_HANDLER_CTX.get_connection(worker.upper(), ConnectionTypeEnum.SESSION)
        async with session.session() as async_session:
            query = select(ChatBotActivity).where(ChatBotActivity.task_code == task_code).limit(1)
            result = await async_session.execute(query)
            data = result.scalars().all()
            return data
