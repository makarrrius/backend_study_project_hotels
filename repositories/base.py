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
            
    async def edit(self, id: int, data: BaseModel) -> None:
        
        db_item = await self.get_one_or_none(id=id)
        if db_item is None:
            raise HTTPException(status_code=404, detail=f"Id {id} not found")
        
        edit_data_stmt = update(self.model).where(self.model.id == id).values(data.model_dump())
        await self.session.execute(edit_data_stmt) 

    async def delete(self, id: int) -> None:
        
        db_item = await self.get_one_or_none(id=id)
        if db_item is None:
            raise HTTPException(status_code=404, detail=f"Id {id} not found")
        
        edit_data_stmt = delete(self.model).where(self.model.id == id)
        await self.session.execute(edit_data_stmt)