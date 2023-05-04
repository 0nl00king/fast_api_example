from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)

from sqlalchemy.orm import sessionmaker

from config import DB_URL


# create async engine for interaction with database
engine = create_async_engine(
    DB_URL,
    future=True,
    echo=True,
)

# create session for the interaction with database
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
