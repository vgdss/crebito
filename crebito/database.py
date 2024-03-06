"""Database connection"""
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import declarative_base

from .config import settings

# Criação do AsyncEngine
async_engine: AsyncEngine = create_async_engine(
    url=settings.db.uri,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
    pool_timeout=settings.db.pool_timeout,
    pool_recycle=settings.db.pool_recycle,
    echo=settings.db.echo,
)

# Configuração do AsyncSession
async_session = async_sessionmaker(
    bind=async_engine, 
    expire_on_commit=False, 
    autoflush=True,
    class_=AsyncSession
)

Base = declarative_base()

async def get_db_session():
    #async with SessionLocal() as session:
    async with async_session() as session:
        yield session
