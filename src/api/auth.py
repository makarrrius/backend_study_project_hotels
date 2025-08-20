from fastapi import APIRouter

from repositories.users import UsersRepository
from src.schemas.users import UserAdd, UserRequestAdd
from src.database import async_session_maker

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])

router.post('/register')
async def register_user(
    data: UserRequestAdd
):
    hashed_password = '1234545'
    new_user_data = UserAdd(email=data.email, username=data.username, password=hashed_password)
    async with async_session_maker() as session: # объявляем асинхронный контекстный менеджер, максимум 100 одновременных подключений, по умолчанию алхимия создает 5 подключ, при нагрузке - доп. 10
        await UsersRepository(session).add(new_user_data)
        await session.commit() # фиксация изменений в бд - не вызывается для select запросов

    return {'status': 'OK'}