from src.schemas.facilities import Facilities
from pydantic import BaseModel, ConfigDict


class RoomsAddRequest(BaseModel):
    hotel_id: int
    title: str
    description: str
    price: int
    quantity: int
    facilities_ids: list[int] = []


class RoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str
    price: int
    quantity: int


class Rooms(RoomsAdd):
    id: int


class RoomsPatchRequest(BaseModel):
    hotel_id: int | None = (None,)
    title: str | None = (None,)
    description: str | None = None
    price: int | None = (None,)
    quantity: int | None = None
    facilities_ids: list[int] = []


class RoomsPatch(BaseModel):
    hotel_id: int | None = (None,)
    title: str | None = (None,)
    description: str | None = None
    price: int | None = (None,)
    quantity: int | None = None


class RoomsWithRels(Rooms):
    facilities: list[Facilities]

    model_config = ConfigDict(from_attributes=True)
