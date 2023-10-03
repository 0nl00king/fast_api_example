from fastapi import Depends

from jose import (
    jwt,
    JWTError,
)

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import OAuth2PasswordBearer

from fastapi import (
    HTTPException,
    status,
)

from config import (
    SECRET_KEY,
    ALGORITHM,
)

from db.core.user import UserDAL

from db.session import get_async_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def _get_user_by_email_for_auth(email: str, session: AsyncSession):
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_email(email=email)


async def get_current_user_from_token(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_async_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e
    user = await _get_user_by_email_for_auth(email=username, session=session)
    if not user:
        raise credentials_exception
    return user
