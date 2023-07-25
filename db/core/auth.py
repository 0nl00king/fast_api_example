from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from db.hashing import Hasher

from api.actions.auth import _get_user_by_email_for_auth
from db.models import User


async def user_auth(
        email: str,
        password: str,
        session: AsyncSession,
) -> Union[User, None]:
    user = await _get_user_by_email_for_auth(email=email, session=session)
    if not user:
        return
    if Hasher.verify_password(password, user.hashed_password):
        return
    return user
