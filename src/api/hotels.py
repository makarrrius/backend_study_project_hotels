from fastapi import Body, Query, APIRouter

from sqlalchemy import insert

from src.schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

# Принимают query и path параметры (get, delete)
# Задание №2: Пагинация для отелей
@router.get("")
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(None, description="Айдишник"),
    title: str | None = Query(None, description="Название отеля")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    first_page_elem_ind = pagination.per_page * (pagination.page - 1)
    last_page_elem_ind = pagination.per_page * pagination.page
    return hotels_[first_page_elem_ind:last_page_elem_ind]

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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump()) # преобразуем модель алхимии (экземпляр класса) в словарь вида {'title':, 'location':}; раскрываем в кварги через 2 *
        await session.execute(add_hotel_stmt) # создаем sql выражение
        await session.commit() # выполняем его

    return {'status': 'OK'}


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
