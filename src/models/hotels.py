from src.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class HotelsOrm(Base):
    """
    Создали модель отелей, отображает реальную таблицу в БД
    """

    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )  # первичный ключ - уникальный столбец
    title: Mapped[str] = mapped_column(
        String(100)
    )  # используем Mapped[int] вместо int, тк используем самую свежую версию Алхимии
    location: Mapped[
        str
    ]  # если не нужно ограничивать количество символов - можно не использовать mapped_column
