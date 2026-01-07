from pydantic import BaseModel, ConfigDict


class FacilitiesAdd(BaseModel):
    title: str

    model_config = ConfigDict(from_attributes=True)


class Facilities(FacilitiesAdd):
    id: int


class RoomFacilitiesAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacilities(RoomFacilitiesAdd):
    id: int
