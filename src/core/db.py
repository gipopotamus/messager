from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from src.core.config import get_settings

settings = get_settings()

engine = create_async_engine(settings.postgres.url, echo=False)
AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()


