from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# НАСТРОЙКА CORS - РАЗРЕШАЕМ ВСЕ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    city: str
    max_price: Optional[int] = None

APARTMENTS = {
    "москва": [
        {"id": 1, "title": "Москва - Патриаршие", "price": 8900, "address": "Москва, Патриаршая, 12"},
        {"id": 2, "title": "Москва - Арбат", "price": 12500, "address": "Москва, Арбат, 8"},
    ],
    "сочи": [
        {"id": 3, "title": "Сочи - У моря", "price": 5200, "address": "Сочи, Приморская, 5"},
        {"id": 4, "title": "Сочи - Адлер", "price": 6100, "address": "Сочи, ул. Ленина, 30"},
    ],
    "казань": [
        {"id": 5, "title": "Казань - Центр", "price": 4900, "address": "Казань, ул. Баумана, 25"},
    ],
}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "ok", "message": "API работает"}

@app.post("/search")
async def search(request: SearchRequest):
    city = request.city.lower()
    apartments = APARTMENTS.get(city, [])
    return {
        "success": True,
        "count": len(apartments),
        "apartments": apartments
    }