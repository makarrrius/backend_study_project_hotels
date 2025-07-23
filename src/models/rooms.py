from src.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

class RoomsOrm(Base):
    """
    Создали модель отелей, отображает реальную таблицу в БД
    """
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True) # первичный ключ - уникальный столбец
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id")) # foreign key = внешний ключ, hotels - название таблицы, id - название столбца
    title: Mapped[str]
    description: Mapped[str | None] # задание опционального параметра в 2 алхимии, в прошлой версии опц. пар-ры задавались так: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int]
    quantity: Mapped[int]
