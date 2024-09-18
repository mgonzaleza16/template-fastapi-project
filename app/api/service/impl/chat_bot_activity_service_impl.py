from typing import Final

from ...repository.chat_bot_activity_repository import ChatBotActivityRepository
from ...repository.impl.chat_bot_activity_impl import ChatBotActivityRepositoryImpl
from ..chat_bot_activity_service import ChatBotActivityService


class ChatBotActivityServiceImpl(ChatBotActivityService):
    chat_bot_activity_repository: Final[ChatBotActivityRepository] = ChatBotActivityRepositoryImpl()

    async def all(self, worker: str) -> list:
        return await self.chat_bot_activity_repository.all(worker)

    async def find_by_task_code(self, worker: str, task_code: str):
        return await self.chat_bot_activity_repository.find_by_task_code(worker, task_code)
