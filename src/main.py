from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.init import redis_manager
from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookigns import router as router_bookings
from src.api.facilities import router as router_facilities
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте приложения
    await redis_manager.connect()
    yield
    await redis_manager.close()
    # При выключении приложения


app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)

# 3 вариант запуска приложения - рекомендуемый (в консоли только python main.py)
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
