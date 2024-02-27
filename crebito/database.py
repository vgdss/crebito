from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql+asyncpg://user:password@127.0.0.1/crebito"

engine: AsyncEngine = create_async_engine(
    url=DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,  # Ajuste conforme necessário
    pool_recycle=1800,  # Recicla conexões a cada 15 minutos
)

SessionLocal: AsyncSession = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()