from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from fastapi.security import OAuth2PasswordRequestForm

from db.session import get_async_session

from db.core.auth import user_auth

from db.security import create_access_token

from config import ACCESS_TOKEN_EXPIRE_MINUTES

from api.schemas.auth import Token

auth_router = APIRouter()


@auth_router.post("/token", response_model=Token)
async def token_auth(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_async_session),
):
    user = await user_auth(
        form_data.username,
        form_data.password,
        session,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
