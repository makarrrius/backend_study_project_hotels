from repositories.hotels import HotelsRepository
from schemas.rooms import RoomsAdd, RoomsPatch
from src.repositories.rooms import RoomsRepository
from src.database import async_session_maker

from fastapi import APIRouter, Body, HTTPException


router = APIRouter(prefix='/hotels', tags=['Номера'])

@router.get('/{hotel_id}/rooms')
async def get_rooms(
    hotel_id: int
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id = hotel_id)
    
@router.post('/rooms')
async def add_rooms(
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
    async with async_session_maker() as session:
        if not await HotelsRepository(session).get_one_or_none(id=room_data.hotel_id):
            raise HTTPException(status_code=409, detail='Отеля с таким hotel_id не существует')
        rooms = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {'status': 'OK', 'data': rooms}

@router.delete('/rooms/{room_id}')
async def delete_room(
    room_id: int
):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id = room_id)
        await session.commit()
    return {'status': 'OK'}

@router.put('/rooms/{room_id}')
async def change_all_room_data(
    room_id: int,
    room_data: RoomsAdd
):
    async with async_session_maker() as session:
        if not await HotelsRepository(session).get_one_or_none(id=room_data.hotel_id):
            raise HTTPException(status_code=409, detail='Отеля с таким hotel_id не существует')
        await RoomsRepository(session).edit(data=room_data, id=room_id)
        await session.commit()
    return {'status': 'OK'}

@router.patch('/rooms/{room_id}')
async def change_all_room_data(
    room_id: int,
    room_data: RoomsPatch
):
    async with async_session_maker() as session:
        if not await HotelsRepository(session).get_one_or_none(id=room_data.hotel_id):
            raise HTTPException(status_code=409, detail='Отеля с таким hotel_id не существует')
        await RoomsRepository(session).edit(data=room_data, id=room_id, exclude_unset=True)
        await session.commit()
    return {'status': 'OK'}