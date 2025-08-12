from pydantic import BaseModel, Field

class HotelAdd(BaseModel):
    title: str
    location: str

class Hotel(HotelAdd):
    id: int

class HotelPatch(BaseModel):
    title: str | None = Field(None), # = None - значение по умолчанию = None, обязательно указывать
    location: str | None = Field(None)