from pydantic import BaseModel


class HotelAdd(BaseModel):
    title: str
    location: str


class Hotel(HotelAdd):
    id: int


class HotelPatch(BaseModel):
    title: str | None = (
        None,
    )  # = None - значение по умолчанию = None, обязательно указывать
    location: str | None = None
