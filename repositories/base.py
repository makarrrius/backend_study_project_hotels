from sqlalchemy import select

class BaseRepository: # задаем базовый класс по паттерну - Репозиторий (DAO)

    model = None

    def __init__(self, session): # открывать на каждый запрос сессию - не эффективно
        self.session = session # будем получать объект сессиию более верхнеуровневно (выше), чтобы при каждом запросе к бд не блокировать множество подлкючений
         
    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model)
        result = await self.session.execute(query, **filter_by)
        return result.scalars().one_or_none()
        