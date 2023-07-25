from enum import Enum
from typing import Union

from sqlalchemy import (
    and_,
    select,
    update,
)

from sqlalchemy.ext.asyncio import AsyncSession

from db.models.user import (
    User,
    PortalRole,
)


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(
            self,
            name: str,
            surname: str,
            email: str,
            hashed_password: str,
            roles: list[PortalRole]
    ) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            hashed_password=hashed_password,
            roles=roles,
        )
        self.session.add(new_user)
        await self.session.flush()
        return new_user

    async def get_user_by_id(self, user_id: int) -> Union[User, None]:
        query = select(User).where(User.user_id == user_id)
        res = await self.session.execute(query)
        user_row = res.fetchone()
        if user_row:
            return user_row[0]

    async def update_user(self, user_id: int, **kwargs) -> Union[int, None]:
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active == True))
            .values(kwargs)
            .returning(User.user_id)
        )
        res = await self.session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row:
            return update_user_id_row[0]

    async def delete_user(self, user_id: int) -> Union[int, None]:
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active == True))
            .values(is_active=False)
            .returning(User.user_id)
        )
        res = await self.session.execute(query)
        delete_user_id_row = res.fetchone()
        if delete_user_id_row:
            return delete_user_id_row[0]

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        query = select(User).where(User.email == email)
        res = await self.session.execute(query)
        user_row = res.fetchone()
        if user_row:
            return user_row[0]
