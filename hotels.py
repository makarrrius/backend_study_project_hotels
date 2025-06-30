from fastapi import Query, Body, APIRouter

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {'id': 1, 'title': 'Sochi', 'name':'sochi'},
    {'id': 2, 'title': 'Dubai', 'name':'dubai'},
]

# Принимают query и path параметры (get, delete)
@router.get("")
def get_hotels(
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
    return hotels_

@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}

# Принимают body, request body (put, patch, post)
@router.post("")
def create_hotel(
    title: str = Body(embed=True)
):
    global hotels
    hotels.append({
         'id': hotels[-1]['id'] + 1,
         'title': title
    })
    return {'status': 'OK'}


# Задача 1
# PUT - ручка, клиент обязан отправить все параметры сущности кроме id, меняем только title и name, обязательно принимаем оба эти параметра
@router.put('/{hotel_id}')
def change_all_hotel_data(
    hotel_id: int,
    title: str = Body(),
    name: str = Body()
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = title
            hotel['name'] = name
    return {'status': 'OK'} 

# Задача 2
# PATCH - ручка, клиент обязан отправить все параметры сущности кроме id, меняем либо title, либо name, либо и то, и то, принимаем параметры опционально
@router.patch('/{hotel_id}')
def change_partly_hotel_data(
    hotel_id: int,
    title: str = Body(None),
    name: str = Body(None)
):
    global hotels
    for hotel in hotels:
        if title and hotel['id'] == hotel_id:
            hotel['title'] = title
        elif name and hotel['id'] == hotel_id:
            hotel['name'] = name
    return {'status': 'OK'} 