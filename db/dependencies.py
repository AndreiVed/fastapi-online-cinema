from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = AsyncSessionLocal()

    try:
        yield db
    finally:
        await db.close()
