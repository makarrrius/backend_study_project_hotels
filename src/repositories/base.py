from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete

class BaseRepository: # задаем базовый класс по паттерну - Репозиторий (DAO)

    model = None
    schema: BaseModel = None

    def __init__(self, session): # открывать на каждый запрос сессию - не эффективно
        self.session = session # будем получать объект сессиию более верхнеуровневно (выше), чтобы при каждом запросе к бд не блокировать множество подлкючений
         
    async def get_all(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()] # преобразование сущности БД в пайдентик схему, чтобы принимать на вход пайдентик схему и ее же отдавать на выход - паттерн DataMapper
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model =  result.scalars().one_or_none()
        if model is None:
            return None
        else:
            return self.schema.model_validate(model, from_attributes=True) # преобразование сущности БД в пайдентик схему, чтобы принимать на вход пайдентик схему и ее же отдавать на выход - паттерн DataMapper
    
    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one() # выполнение sql запроса внутри транзакции
        return self.schema.model_validate(model, from_attributes=True) # преобразование сущности БД в пайдентик схему, чтобы принимать на вход пайдентик схему и ее же отдавать на выход - паттерн DataMapper
            
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