from datetime import date
from fastapi import Body, Query, APIRouter

from src.services.hotels import HotelService
from src.schemas.hotels import HotelAdd, HotelPatch
from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException
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
    return await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )


@router.get("/{hotel_id}")
async def get_hotels_by_id(
    hotel_id: int,
    db: DBDep,
):
    try:
        return await HotelService.get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}


# Принимают body, request body (put, patch, post)
@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звезд у моря",
                    "location": "ул. Моря 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {"title": "Отель Дубай у фонтана", "location": "ул. Шейха 2"},
            },
        }
    ),
):
    hotel = await HotelService(db).create_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def change_all_hotel_data(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await HotelService(db).change_all_hotel_data(hotel_id, hotel_data)
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def change_partly_hotel_data(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    await HotelService(db).change_partly_hotel_data(hotel_id, hotel_data)
    return {"status": "OK"}
