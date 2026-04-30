from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

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


# ============================================
# ВАШИ 50 КВАРТИР (оставляем как есть)
# ============================================
REAL_APARTMENTS = [
    # ... все ваши квартиры (не меняйте) ...
]


def get_city_from_address(address: str) -> str:
    address_lower = address.lower()
    if "москва" in address_lower:
        return "москва"
    elif "сочи" in address_lower:
        return "сочи"
    elif "санкт-петербург" in address_lower or "спб" in address_lower:
        return "санкт-петербург"
    elif "казань" in address_lower:
        return "казань"
    else:
        return "москва"


# Группировка по городам
APARTMENTS_BY_CITY = {}
for apt in REAL_APARTMENTS:
    city = get_city_from_address(apt.get("address", ""))
    if city not in APARTMENTS_BY_CITY:
        APARTMENTS_BY_CITY[city] = []
    APARTMENTS_BY_CITY[city].append(apt)

print(f"📊 Загружено квартир: {len(REAL_APARTMENTS)}")
print(f"🏙️ Города: {list(APARTMENTS_BY_CITY.keys())}")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {"status": "ok", "cities": list(APARTMENTS_BY_CITY.keys())}


@app.post("/search")
async def search(request: SearchRequest):
    city = request.city.lower()
    apartments = APARTMENTS_BY_CITY.get(city, [])

    # ФИЛЬТРАЦИЯ ПО ЦЕНЕ
    if request.max_price and request.max_price > 0:
        apartments = [apt for apt in apartments if apt.get("price", 0) <= request.max_price]
        print(f"💰 Фильтр: цены до {request.max_price} ₽, осталось {len(apartments)} квартир")

    return {
        "success": True,
        "count": len(apartments),
        "apartments": apartments
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)