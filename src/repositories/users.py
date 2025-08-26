from pydantic import EmailStr
from sqlalchemy import select
from src.schemas.users import User, UserWithHashedPassword
from src.models.users import UsersOrm
from src.repositories.base import BaseRepository

class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_user_with_hashed_password(self, email: EmailStr):

        query = select(self.model).filter_by(email = email)
        result = await self.session.execute(query)
        model =  result.scalars().one_or_none()
        if model is None:
            return None
        else:
            return UserWithHashedPassword.model_validate(model, from_attributes=True) # преобразование сущности БД в пайдентик схему, чтобы принимать на вход пайдентик схему и ее же отдавать на выход - паттерн DataMapper
    