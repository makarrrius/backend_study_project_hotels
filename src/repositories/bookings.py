from datetime import date
from sqlalchemy import select

from src.repositories.mappers.mappers import BookingDataMapper
from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    async def get_bookings_with_today_check_in(self):
        query = select(BookingsORM.filter(BookingsORM.date_from == date.today()))

        res = self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()
        ]
