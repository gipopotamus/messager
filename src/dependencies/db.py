from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import AsyncSessionFactory


async def get_db() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session
