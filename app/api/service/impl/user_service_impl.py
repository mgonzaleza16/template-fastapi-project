from typing import Final

from ...dto.user_dto import UserDto
from ...repository.impl.user_repository_impl import UserRepositoryImpl
from ...repository.user_repository import UserRepository
from ..user_service import UserService


class UserServiceImpl(UserService):
    user_repository: Final[UserRepository] = UserRepositoryImpl()

    async def all(self) -> list[UserDto]:
        return await self.user_repository.all()

    async def find_by_email(self, email: str) -> UserDto:
        return await self.user_repository.find_by_email(email)

    @staticmethod
    def format_user_name(first_name: str, last_name: str) -> str:
        return f"{first_name.capitalize()} {last_name.capitalize()}"
