# from api.dependencies import get_current_user_id
from src.models.bookings import BookingsORM
from src.schemas.bookings import Bookings
from repositories.base import BaseRepository

class BookingsRepository(BaseRepository):
    model = BookingsORM
    schema = Bookings