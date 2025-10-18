from api.dependencies import DBDep
from schemas.rooms import RoomsAdd, RoomsPatch

from fastapi import APIRouter, Body, HTTPException


router = APIRouter(prefix='/hotels', tags=['Номера'])

@router.get('/{hotel_id}/rooms')
async def get_rooms(
    db: DBDep,
    hotel_id: int
):
    return await db.rooms.get_all(hotel_id = hotel_id)
    
@router.post('/rooms')
async def add_rooms(
    db: DBDep,
    room_data: RoomsAdd = Body(openapi_examples={
        "1": {
        "summary": "Пример 1",
        "value" : {
            "hotel_id": 1,
            "title" : "Тип 1_Эконом",
            "description": "Бюджетный вариант проживания",
            "price": 10000,
            "quantity": 3
            }
        },
        "2": {
        "summary": "Пример 2",
        "value" : {
            "hotel_id": 2,
            "title" : "Тип 2_Комфорт",
            "description": "Комфортный вариант проживания",
            "price": 20000,
            "quantity": 4
            }
        },
        "3": {
        "summary": "Пример 3",
        "value" : {
            "hotel_id": 3,
            "title" : "Тип 3_Бизнес",
            "description": "Люксовый вариант проживания",
            "price": 50000,
            "quantity": 4
            }
        }
    })
):
    if not await db.hotels.get_one_or_none(id=room_data.hotel_id):
        raise HTTPException(status_code=409, detail='Отеля с таким hotel_id не существует')
    rooms = await db.rooms.add(room_data)
    await db.commit()
    return {'status': 'OK', 'data': rooms}

@router.delete('/rooms/{room_id}')
async def delete_room(
    db: DBDep,
    room_id: int
):
    await db.rooms.delete(id = room_id)
    await db.commit()
    return {'status': 'OK'}

@router.put('/rooms/{room_id}')
async def change_all_room_data(
    db: DBDep,
    room_id: int,
    room_data: RoomsAdd
):
    if not await db.hotels.get_one_or_none(id=room_data.hotel_id):
        raise HTTPException(status_code=409, detail='Отеля с таким hotel_id не существует')
    await db.rooms.edit(data=room_data, id=room_id)
    await db.commit()
    return {'status': 'OK'}

@router.patch('/rooms/{room_id}')
async def change_all_room_data(
    db: DBDep,
    room_id: int,
    room_data: RoomsPatch
):
    if not await db.hotels.get_one_or_none(id=room_data.hotel_id):
        raise HTTPException(status_code=409, detail='Отеля с таким hotel_id не существует')
    await db.rooms.edit(data=room_data, id=room_id, exclude_unset=True)
    await db.commit()
    return {'status': 'OK'}