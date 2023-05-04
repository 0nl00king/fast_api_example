from sqlalchemy.ext.asyncio import AsyncSession

from db.models.user import User


class UserDAL:
    """ Data Access Layer for operating user info """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, name: str, surname: str, email: str) -> User:
        new_user = User(name=name, surname=surname, email=email)
        self.session.add(new_user)
        await self.session.flush()
        return new_user
