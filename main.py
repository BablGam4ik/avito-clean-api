from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# РАЗРЕШАЕМ ЗАПРОСЫ С ЛЮБЫХ САЙТОВ (включая Beget)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # * означает "все сайты"
    allow_credentials=True,
    allow_methods=["*"],  # разрешаем все методы (GET, POST и т.д.)
    allow_headers=["*"],  # разрешаем все заголовки
)

class SearchRequest(BaseModel):
    city: str

# ДАННЫЕ ДЛЯ ГОРОДОВ
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

@app.post("/search")
async def search(request: SearchRequest):
    city = request.city.lower()
    data = APARTMENTS.get(city, [])
    return {"success": True, "count": len(data), "apartments": data}