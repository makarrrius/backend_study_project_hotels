from datetime import date
from fastapi import Body, Query, APIRouter

from src.schemas.hotels import Hotel, HotelAdd, HotelPatch
from src.api.dependencies import DBDep, PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(example="2025-08-01"),
    date_to: date = Query(example="2025-08-10"),
):
    return await db.hotels.get_filtered_by_time(
        location=location,
        title=title,
        date_from=date_from,
        date_to=date_to,
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1)
    )
    
@router.get("/{hotel_id}")
async def get_hotels(
    hotel_id: int,
    db: DBDep,
):
    return await db.hotels.get_one_or_none(id = hotel_id)

@router.delete("/{hotel_id}")
async def delete_hotel(
    db: DBDep,
    hotel_id: int
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()    
    return {'status': 'OK'}

# Принимают body, request body (put, patch, post)
@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(openapi_examples={
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit() # фиксация изменений в бд - не вызывается для select запросов
    return {'status': 'OK', "data": hotel}

@router.put('/{hotel_id}')
async def change_all_hotel_data(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelAdd
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit() # фиксация изменений в бд - не вызывается для select запросов
    return {'status': 'OK'}

@router.patch('/{hotel_id}')
async def change_partly_hotel_data(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPatch
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit() # фиксация изменений в бд - не вызывается для select запросов
    return {'status': 'OK'}
