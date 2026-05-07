from datetime import date

from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundException
from src.schemas.hotels import HotelAdd, HotelPatch, Hotel
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_time(
        self,
        pagination,
        location: str | None,
        title: str | None,
        date_from: date,
        date_to: date,
    ):
        check_date_to_after_date_from(date_from, date_to)  
        return await self.db.hotels.get_filtered_by_time(
            location=location,
            title=title,
            date_from=date_from,
            date_to=date_to,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1),
        )
    
    async def get_hotel(
        self,
        hotel_id: int
    ):
        return await self.db.hotels.get_one_or_none(id=hotel_id)
    
    async def create_hotel(
        self,
        hotel_data: HotelAdd,
    ):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel
    
    async def change_all_hotel_data(
        self,
        hotel_id: int, 
        hotel_data: HotelAdd
    ):
        await self.db.hotels.edit(hotel_data, id=hotel_id)
        await self.db.commit()

    async def change_partly_hotel_data(
        self,
        hotel_id: int, 
        hotel_data: HotelPatch
    ):
        await self.db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    async def delete_hotel(
        self,
        hotel_id: int
    ):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
    
    async def get_hotel_with_check(self, hotel_id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
