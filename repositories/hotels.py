from sqlalchemy import select
from src.models.hotels import HotelsOrm
from repositories.base import BaseRepository

class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ):
        
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
        
        return result.scalars().all()
    