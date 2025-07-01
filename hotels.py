from fastapi import Query, APIRouter

from schemas.hotels import Hotel, HotelPatch
from dependencies import PaginationDep

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
def create_hotel(
    hotel_data: Hotel
):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': hotel_data.title,
        'name': hotel_data.name
    })
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