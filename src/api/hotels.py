from fastapi import Body, Query, APIRouter

from repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep
from src.database import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Отели"])

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
    
@router.get("/{hotel_id}")
async def get_hotels(
    hotel_id: int
):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id = hotel_id)

@router.delete("/{hotel_id}")
async def delete_hotel(
    hotel_id: int
):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()    
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

@router.put('/{hotel_id}')
async def change_all_hotel_data(
    hotel_id: int,
    hotel_data: Hotel
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit() # фиксация изменений в бд - не вызывается для select запросов
    return {'status': 'OK'}

@router.patch('/{hotel_id}')
async def change_partly_hotel_data(
    hotel_id: int,
    hotel_data: HotelPatch
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit() # фиксация изменений в бд - не вызывается для select запросов
    return {'status': 'OK'}
