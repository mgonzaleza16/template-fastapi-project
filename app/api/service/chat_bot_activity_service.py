from abc import ABC, abstractmethod


class ChatBotActivityService(ABC):

    @abstractmethod
    async def all(self, worker: str) -> list:
        pass

    @abstractmethod
    async def find_by_task_code(self, worker: str, task_code: str):
        pass
