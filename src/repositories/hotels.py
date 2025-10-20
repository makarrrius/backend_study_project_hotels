from datetime import date
from sqlalchemy import select
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository

class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    # async def get_all(
    #         self,
    #         location,
    #         title,
    #         limit,
    #         offset,
    # ) -> list[Hotel]:
        
    #     query = select(HotelsOrm)
        
    #     if title:
    #         query = query.filter(HotelsOrm.title.ilike(f'%{title}%'))
    #     if location:
    #         query = query.filter(HotelsOrm.location.ilike(f'%{location}%'))
    #     query = (
    #         query
    #         .limit(limit)
    #         .offset(offset)
    #     )

    #     print(query.compile(compile_kwargs={"literal_binds": True}))    
    #     result = await self.session.execute(query)
        
    #     return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
    
    async def get_filtered_by_time(
        self,
        location: str | None,
        title: str | None,
        limit: int,
        offset: int,
        date_from: date, 
        date_to: date
    ):

        if title:
            query = query.filter(HotelsOrm.title.ilike(f'%{title}%'))
        if location:
            query = query.filter(HotelsOrm.location.ilike(f'%{location}%'))
        
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        query = select(HotelsOrm)
        if title:
            query = query.filter(HotelsOrm.title.ilike(f'%{title}%'))
        if location:
            query = query.filter(HotelsOrm.location.ilike(f'%{location}%'))
        
        query = (
            query
            .filter(HotelsOrm.id.in_(hotels_ids_to_get))
            .limit(limit)
            .offset(offset)
        )
        
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
    