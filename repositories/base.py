from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete

class BaseRepository: # задаем базовый класс по паттерну - Репозиторий (DAO)

    model = None

    def __init__(self, session): # открывать на каждый запрос сессию - не эффективно
        self.session = session # будем получать объект сессиию более верхнеуровневно (выше), чтобы при каждом запросе к бд не блокировать множество подлкючений
         
    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
    
    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        return result.scalars().one() # выполнение sql запроса внутри транзакции
            
    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None: 
        edit_data_stmt = (
            update(self.model).
            filter_by(**filter_by).
            values(data.model_dump(exclude_unset=exclude_unset)) # если в body пользователь не пришлет какой-то параметр, то алхимия его в бд не обновит
        )
        await self.session.execute(edit_data_stmt)

    async def delete(self, **filter_by) -> None:        
        delete_data_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_data_stmt)