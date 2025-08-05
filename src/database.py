from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine 
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

engine = create_async_engine(settings.db_url) # 1ый вариант дебага алхимии - через параметр echo = True

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase): # просто создаем этот класс и будем от него в разных частях кода наследоваться
    pass