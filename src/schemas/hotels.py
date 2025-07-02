from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str
    name: str

class HotelPatch(BaseModel):
    title: str | None = Field(None), # = None - значение по умолчанию = None, обязательно указывать
    name: str | None = Field(None)