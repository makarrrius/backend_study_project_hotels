from src.schemas.facilities import Facilities
from src.models.facilities import FacilitiesORM
from src.repositories.base import BaseRepository

class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facilities