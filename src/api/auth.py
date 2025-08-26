from fastapi import APIRouter, HTTPException, Response

from services.auth import AuthService
from src.repositories.users import UsersRepository
from src.schemas.users import UserAdd, UserRequestAdd, UserRequestLogin
from src.database import async_session_maker

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])

@router.post('/register')
async def register_user(
    data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, username=data.username, hashed_password=hashed_password)
    async with async_session_maker() as session: # объявляем асинхронный контекстный менеджер, максимум 100 одновременных подключений, по умолчанию алхимия создает 5 подключ, при нагрузке - доп. 10
        await UsersRepository(session).add(new_user_data)
        await session.commit() # фиксация изменений в бд - не вызывается для select запросов

    return {'status': 'OK'}

@router.post("/login")
async def login_user(
    data: UserRequestLogin,
    response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail='Пользователь с таким email не зарегистрирован')
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Пароль не верный')
        
        access_token = AuthService().create_access_token({'user_id':user.id})
        response.set_cookie('access_token', access_token)
        return {'access_token': access_token}