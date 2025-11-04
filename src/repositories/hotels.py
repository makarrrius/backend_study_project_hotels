from datetime import date
from sqlalchemy import select
from src.repositories.mappers.mappers import HotelDataMapper
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository

class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper
    
    async def get_filtered_by_time(
        self,
        location: str | None,
        title: str | None,
        limit: int,
        offset: int,
        date_from: date, 
        date_to: date
    ):
        
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        
        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids_to_get))
        if title:
            query = query.filter(HotelsOrm.title.ilike(f'%{title}%'))
        if location:
            query = query.filter(HotelsOrm.location.ilike(f'%{location}%'))
        
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]
    