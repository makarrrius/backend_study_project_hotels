from sqlalchemy import select
from src.schemas.hotels import Hotel
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository

class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ) -> list[Hotel]:
        
        query = select(HotelsOrm)
        
        if title:
            query = query.filter(HotelsOrm.title.ilike(f'%{title}%'))
        if location:
            query = query.filter(HotelsOrm.location.ilike(f'%{location}%'))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        print(query.compile(compile_kwargs={"literal_binds": True}))    
        result = await self.session.execute(query)
        
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
    