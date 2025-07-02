from fastapi import Depends, Query
from pydantic import BaseModel

from typing import Annotated

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="Страница")]
    per_page: Annotated[int | None, Query(5, ge=1, le=100, description="Кол-во элементов на странице")]

PaginationDep = Annotated[PaginationParams, Depends()]
