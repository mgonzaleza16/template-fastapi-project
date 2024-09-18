from ..user_repository import UserRepository


class UserRepositoryExcelImpl(UserRepository):
    async def all(self):
        pass

    async def find_by_email(self, email: str):
        pass
