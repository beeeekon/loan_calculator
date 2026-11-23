import logging
from fastapi import FastAPI
from app.api.routers.calculator import router as calc_router


logging.basicConfig(level=logging.INFO)

# Создаем приложение
app = FastAPI(title="Loan Calculator API")
app.include_router(calc_router)

@app.get("/")
def root():
    return {"message": "Сервер работает"}

