from fastapi import APIRouter, HTTPException, Request, Response

from src.api.dependencies import DBDep, UserIdDep
from src.services.auth import AuthService
from src.schemas.users import UserAdd, UserRequestAdd, UserRequestLogin

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])

@router.post('/register')
async def register_user(
    db: DBDep,
    data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, username=data.username, hashed_password=hashed_password)
    await db.users.add(new_user_data)
    await db.commit() # фиксация изменений в бд - не вызывается для select запросов

    return {'status': 'OK'}

@router.post("/login")
async def login_user(
    db: DBDep,
    data: UserRequestLogin,
    response: Response
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail='Пользователь с таким email не зарегистрирован')
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Пароль не верный')
    
    access_token = AuthService().create_access_token({'user_id':user.id})
    response.set_cookie('access_token', access_token)
    return {'access_token': access_token}

@router.get("/me")
async def get_me(
    db: DBDep,
    user_id: UserIdDep
):
    user = await db.users.get_one_or_none(id=user_id)
    return user
    
@router.post("/logout")
async def logout_user(
    response: Response
):
    response.delete_cookie('access_token')
    return {'status': 'OK'}