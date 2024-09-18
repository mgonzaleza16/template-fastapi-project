from abc import ABC, abstractmethod

from ..dto.user_dto import UserDto


class UserRepository(ABC):

    @abstractmethod
    async def all(self) -> list[UserDto]:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> UserDto:
        pass
