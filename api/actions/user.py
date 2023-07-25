from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.user import (
    ShowUser,
    UserCreate,
)
from db.core.user import UserDAL
from db.hashing import Hasher
from db.models.user import (
    PortalRole,
    User,
)


async def _create_new_user(body: UserCreate, session: AsyncSession) -> ShowUser:
    async with session.begin():
        user = await UserDAL(session).create_user(
            name=body.name,
            surname=body.surname,
            email=body.email,
            hashed_password=Hasher.get_password_hash(body.password),
            roles=[PortalRole.ROLE_PORTAL_USER, ],
        )
        return ShowUser(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )


async def _get_user_by_id(
        user_id: int,
        session: AsyncSession,
) -> Union[User, None]:
    async with session.begin():
        user = await UserDAL(session).get_user_by_id(user_id=user_id)
    if user is not None:
        return user


async def _delete_user(user_id: int, session: AsyncSession) -> Union[int, None]:
    async with session.begin():
        return await UserDAL(session).delete_user(user_id=user_id)


async def _update_user(
        updated_user_params: dict,
        user_id: int,
        session: AsyncSession,
) -> Union[int, None]:
    async with session.begin():
        return await UserDAL(session).update_user(
            user_id=user_id,
            **updated_user_params,
        )
