from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
