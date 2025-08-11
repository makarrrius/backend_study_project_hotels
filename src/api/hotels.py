from fastapi import Body, Query, APIRouter

from sqlalchemy import insert, select

from repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm

router = APIRouter(prefix="/hotels", tags=["Отели"])

# Принимают query и path параметры (get, delete)
# Задание №4: Фильтрация по подстроке
@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Расположение отеля")
):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location, 
            title, 
            limit=pagination.per_page, 
            offset=pagination.per_page * (pagination.page - 1)
        )

@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}

# Принимают body, request body (put, patch, post)
@router.post("")
async def create_hotel(
    hotel_data: Hotel = Body(openapi_examples={
        "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель Сочи 5 звезд у моря",
            "location": "ул. Моря 1"
            }
        },
        "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Дубай у фонтана",
            "location": "ул. Шейха 2"
            }
        }
    })
):
    async with async_session_maker() as session: # объявляем асинхронный контекстный менеджер, максимум 100 одновременных подключений, по умолчанию алхимия создает 5 подключ, при нагрузке - доп. 10
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit() # фиксация изменений в бд - не вызывается для select запросов

    return {'status': 'OK', "data": hotel}


# Задача 1
# PUT - ручка, клиент обязан отправить все параметры сущности кроме id, меняем только title и name, обязательно принимаем оба эти параметра
@router.put('/{hotel_id}')
def change_all_hotel_data(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = hotel_data.title
            hotel['name'] = hotel_data.name
    return {'status': 'OK'} 

# Задача 2
# PATCH - ручка, клиент обязан отправить все параметры сущности кроме id, меняем либо title, либо name, либо и то, и то, принимаем параметры опционально
@router.patch('/{hotel_id}')
def change_partly_hotel_data(
    hotel_id: int,
    hotel_data: HotelPatch
):
    global hotels
    for hotel in hotels:
        if hotel_data.title and hotel['id'] == hotel_id:
            hotel['title'] = hotel_data.title
        elif hotel_data.name and hotel['id'] == hotel_id:
            hotel['name'] = hotel_data.name
    return {'status': 'OK'} 
