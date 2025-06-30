import uvicorn
from fastapi import FastAPI

from hotels import router as router_hotels

app = FastAPI()

app.include_router(router_hotels)

# 3 вариант запуска приложения - рекомендуемый (в консоли только python main.py)
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)