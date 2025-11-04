from datetime import date
from src.schemas.facilities import RoomFacilitiesAdd
from src.api.dependencies import DBDep
from src.schemas.rooms import RoomsAdd, RoomsAddRequest, RoomsPatch, RoomsPatchRequest

from fastapi import APIRouter, Body, HTTPException, Query


router = APIRouter(prefix='/hotels', tags=['Номера'])

@router.get('/{hotel_id}/rooms')
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example='2024-08-01'),
    date_to: date = Query(example='2024-08-10')
):
    return await db.rooms.get_filtered_by_time(hotel_id = hotel_id, date_from=date_from, date_to=date_to)

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)
    
@router.post('/rooms')
async def add_rooms(
    db: DBDep,
    room_data: RoomsAddRequest = Body(openapi_examples={
        "1": {
        "summary": "Пример 1",
        "value" : {
            "hotel_id": 1,
            "title" : "Тип 1_Эконом",
            "description": "Бюджетный вариант проживания",
            "price": 10000,
            "quantity": 3,
            "facilities_ids": [1,2]
            }
        },
        "2": {
        "summary": "Пример 2",
        "value" : {
            "hotel_id": 2,
            "title" : "Тип 2_Комфорт",
            "description": "Комфортный вариант проживания",
            "price": 20000,
            "quantity": 4,
            "facilities_ids": [1]
            }
        },
        "3": {
        "summary": "Пример 3",
        "value" : {
            "hotel_id": 3,
            "title" : "Тип 3_Бизнес",
            "description": "Люксовый вариант проживания",
            "price": 50000,
            "quantity": 4,
            "facilities_ids": [2]
            }
        }
    })
    
):
    _room_data = RoomsAdd(**room_data.model_dump())

    if not await db.hotels.get_one_or_none(id=room_data.hotel_id):
        raise HTTPException(status_code=409, detail='Отеля с таким hotel_id не существует')
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [RoomFacilitiesAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {'status': 'OK', 'data': room}

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
    room_data: RoomsAddRequest
):
    _room_data = RoomsAdd(**room_data.model_dump())
    if not await db.hotels.get_one_or_none(id=room_data.hotel_id):
        raise HTTPException(status_code=409, detail='Отеля с таким hotel_id не существует')
    
    await db.rooms.edit(data=_room_data, id=room_id)
    await db.rooms_facilities.set_room_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {'status': 'OK'}

@router.patch('/rooms/{room_id}')
async def change_partly_room_data(
    db: DBDep,
    room_id: int,
    room_data: RoomsPatchRequest
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomsPatch(**_room_data_dict)
    
    if not await db.hotels.get_one_or_none(id=room_data.hotel_id):
        raise HTTPException(status_code=409, detail='Отеля с таким hotel_id не существует')
    
    await db.rooms.edit(data=_room_data, id=room_id, exclude_unset=True)
    
    if 'facilities_ids' in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(room_id=room_id, facilities_ids=_room_data_dict['facilities_ids'])
    
    await db.commit()
    return {'status': 'OK'}