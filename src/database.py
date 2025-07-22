from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import text
import asyncio

from src.config import settings

engine = create_async_engine(settings.db_url)

async def func():
    async with engine.begin() as conn:
        res = await conn.execute(text("SELECT version()"))
        print(res.fetchone())

asyncio.run(func())