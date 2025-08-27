from fastapi import HTTPException
from repositories.hotels import HotelsRepository
from src.schemas.rooms import Rooms
from src.models.rooms import RoomsOrm
from repositories.base import BaseRepository

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms