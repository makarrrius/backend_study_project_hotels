# from api.dependencies import get_current_user_id
from src.models.bookings import BookingsORM
from src.schemas.bookings import Bookings, BookingsAdd
from repositories.base import BaseRepository
from repositories.users import UsersRepository

class BookingsRepository(BaseRepository):
    model = BookingsORM
    schema = Bookings