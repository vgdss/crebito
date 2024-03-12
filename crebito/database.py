"""Database connection"""
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import declarative_base

# Criação do AsyncEngine
engine: AsyncEngine = create_async_engine(
    url="postgresql+asyncpg://user:password@127.0.0.1/crebito",
    pool_size=15,
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=1800,
    echo=False,
)

# Configuração do AsyncSession
async_session = async_sessionmaker(
    bind=engine, 
    expire_on_commit=False, 
    autoflush=True,
    class_=AsyncSession
)

Base = declarative_base()

async def get_db_session():
    #async with SessionLocal() as session:
    async with async_session() as session:
        yield session
