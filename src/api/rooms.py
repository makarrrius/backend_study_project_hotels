from datetime import date
from src.api.dependencies import DBDep
from src.schemas.rooms import RoomsAddRequest, RoomsPatchRequest
from src.exceptions import HotelNotFoundHTTPException, \
    RoomNotFoundHTTPException, RoomNotFoundException, HotelNotFoundException
from src.schemas.rooms import RoomsAddRequest, RoomsPatchRequest
from src.services.rooms import RoomService

from fastapi import APIRouter, Body, Query


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomsAddRequest = Body()):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
        return {"status": "OK", "data": room}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.delete("/rooms/{room_id}")
async def delete_room(db: DBDep, room_id: int):
    await db.rooms.delete(id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomsAddRequest,
    db: DBDep,
):
    await RoomService(db).edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomsPatchRequest,
    db: DBDep,
):
    await RoomService(db).partially_edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}