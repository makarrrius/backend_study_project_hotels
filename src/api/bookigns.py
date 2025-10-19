from fastapi import APIRouter, Body

from api.dependencies import DBDep, PaginationDep, UserIdDep
from schemas.bookings import BookingsAdd, BookingsAddRequest

router = APIRouter(prefix='/bookings', tags = ['Бронирования'])

@router.get("")
async def get_all_bookings(
    db: DBDep
):
    return await db.bookings.get_all()

@router.get("/me")
async def get_bookings_for_user(
    db: DBDep,
    user_id: UserIdDep
):
    return await db.bookings.get_all(user_id=user_id)

@router.post("")
async def add_booking(
    db: DBDep,
    user_id: UserIdDep, # проверяем, что пользователь залогинен и получаем отсюда user_id
    booking_data: BookingsAddRequest = Body()
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price = room.price
    _booking_data = BookingsAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit() # фиксация изменений в бд - не вызывается для select запросов
    return {'status': 'OK', "data": booking}
