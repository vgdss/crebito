from sqlalchemy import QueuePool
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql+asyncpg://user:password@127.0.0.1/crebito"

engine: AsyncEngine = create_async_engine(
    url=DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    poolclass=QueuePool,
)

SessionLocal: AsyncSession = async_sessionmaker(
    bind=engine, 
    expire_on_commit=False,
    autoflush=True,
    class_=AsyncSession,
)

Base = declarative_base()


async def get_db_session():
    async with SessionLocal() as session:
        yield session
