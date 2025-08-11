from pydantic import BaseModel
from sqlalchemy import select, insert

class BaseRepository: # задаем базовый класс по паттерну - Репозиторий (DAO)

    model = None

    def __init__(self, session): # открывать на каждый запрос сессию - не эффективно
        self.session = session # будем получать объект сессиию более верхнеуровневно (выше), чтобы при каждом запросе к бд не блокировать множество подлкючений
         
    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model)
        result = await self.session.execute(query, **filter_by)
        return result.scalars().one_or_none()
    
    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        return result.scalars().one() # выполнение sql запроса внутри транзакции