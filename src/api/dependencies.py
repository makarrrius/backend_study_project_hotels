from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel

from typing import Annotated

from services.auth import AuthService

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="Страница")]
    per_page: Annotated[int | None, Query(5, ge=1, le=100, description="Кол-во элементов на странице")]

PaginationDep = Annotated[PaginationParams, Depends()]

def get_token(request: Request):
    access_token = request.cookies.get('access_token', None)
    if not access_token:
        raise HTTPException(status_code=401, detail='Вы не предоставили токен доступа')
    return access_token

def get_current_user_id(access_token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(access_token)
    return data.get('user_id')


UserIdDep = Annotated[int, Depends(get_current_user_id)] # int = user_id

