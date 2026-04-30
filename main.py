from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

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
# ВАШИ 50 КВАРТИР (вставьте сюда свои данные)
# ============================================
REAL_APARTMENTS = [
    # ... ваши квартиры из avito_apartments.json
]


def get_city_from_address(address: str) -> str:
    return "москва"


APARTMENTS_BY_CITY = {"москва": REAL_APARTMENTS}

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

    # Фильтр по цене (безопасная версия)
    if request.max_price is not None and request.max_price > 0:
        filtered = []
        for apt in apartments:
            price = apt.get("price", 0)
            if price <= request.max_price:
                filtered.append(apt)
        apartments = filtered

    return {
        "success": True,
        "count": len(apartments),
        "apartments": apartments
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)