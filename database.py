from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./cookbook.db"

engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронная зависимость FastAPI, предоставляющая сессию БД на время запроса."""
    async with AsyncSessionLocal() as session:
        yield session
