from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager
from src.database import async_session_maker


async def test_add_hotel():
    hotel_data = HotelAdd(title="Test Hotel", description="Test Description")
    async with DBManager(session_factory=async_session_maker) as db:
        new_hotel_data = await db.bookings.add(hotel_data)
        print(f"{new_hotel_data=}")
