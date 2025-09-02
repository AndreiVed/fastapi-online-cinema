from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from db.database import SessionLocal


async def get_db():
    async with SessionLocal() as session:
        yield session
