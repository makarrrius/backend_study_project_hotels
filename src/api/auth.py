from fastapi import APIRouter

from src.repositories.users import UsersRepository
from src.schemas.users import UserAdd, UserRequestAdd
from src.database import async_session_maker

from passlib.context import CryptContext

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/register')
async def register_user(
    data: UserRequestAdd
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, username=data.username, hashed_password=hashed_password)
    async with async_session_maker() as session: # объявляем асинхронный контекстный менеджер, максимум 100 одновременных подключений, по умолчанию алхимия создает 5 подключ, при нагрузке - доп. 10
        await UsersRepository(session).add(new_user_data)
        await session.commit() # фиксация изменений в бд - не вызывается для select запросов

    return {'status': 'OK'}