from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,async_sessionmaker
from collections.abc import AsyncGenerator
from app.config import settings

engine = create_async_engine(url=settings.database_url, echo=True, pool_size=10, max_overflow=20)
async_session = async_sessionmaker(engine, expire_on_commit=False, autoflush=False, class_=AsyncSession)

async def get_db()->AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session