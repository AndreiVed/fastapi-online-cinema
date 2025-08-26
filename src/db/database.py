from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./online_cinema.db"

engine = create_async_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=True, future=True
)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    future=True,
)

Base = declarative_base()
