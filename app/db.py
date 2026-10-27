from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import get_settings
s=get_settings(); engine=create_async_engine(s.database_url); SessionLocal=async_sessionmaker(engine,expire_on_commit=False)
class Base(DeclarativeBase): pass
async def get_db()->AsyncGenerator[AsyncSession,None]:
    async with SessionLocal() as session: yield session
