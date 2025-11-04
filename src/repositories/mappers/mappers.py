from src.models.facilities import FacilitiesORM
from src.schemas.facilities import Facilities
from src.schemas.rooms import Rooms
from src.models.users import UsersOrm
from src.schemas.users import User
from src.models.bookings import BookingsORM
from src.models.rooms import RoomsOrm
from src.models.hotels import HotelsOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.hotels import Hotel


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel

class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Rooms

class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User

class BookingDataMapper(DataMapper):
    db_model = BookingsORM
    schema = Hotel

class FacilityDataMapper(DataMapper):
    db_model = FacilitiesORM
    schema = Facilities