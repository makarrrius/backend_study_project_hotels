import uvicorn
from fastapi import FastAPI

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as router_hotels
from src.config import settings

app = FastAPI()

app.include_router(router_hotels)

# 3 вариант запуска приложения - рекомендуемый (в консоли только python main.py)
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
