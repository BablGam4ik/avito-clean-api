from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== НАСТРОЙКИ ДЛЯ ОТПРАВКИ ПИСЕМ =====
SMTP_SERVER = "smtp.yandex.ru"
SMTP_PORT = 465
SMTP_EMAIL = "korpachev-2000@mail.ru"
SMTP_PASSWORD = "lfca okpl gzkq bayh"
ADMIN_EMAIL = "korpacevegor@gmail.com"


# ========================================

class SearchRequest(BaseModel):
    city: str
    max_price: Optional[int] = None


class BookingRequest(BaseModel):
    apartment: dict
    guest_name: str
    guest_phone: str
    guest_email: str
    comment: str
    checkin: str
    checkout: str


# ============================================
# ВАШИ 50 КВАРТИР (оставьте как есть)
# ============================================
REAL_APARTMENTS = [
    # ... все ваши квартиры ...
]


def get_city_from_address(address: str) -> str:
    return "москва"


APARTMENTS_BY_CITY = {"москва": REAL_APARTMENTS}

print(f"📊 Загружено квартир: {len(REAL_APARTMENTS)}")
print(f"🏙️ Города: {list(APARTMENTS_BY_CITY.keys())}")


def send_booking_email(booking: BookingRequest):
    """Функция для отправки письма"""
    subject = "Новая заявка на бронирование квартиры"

    message = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 НОВАЯ ЗАЯВКА НА БРОНИРОВАНИЕ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏠 КВАРТИРА:
Название: {booking.apartment.get('title', 'Не указано')}
Адрес: {booking.apartment.get('address', 'Не указан')}
Цена: {booking.apartment.get('price', 0):,} ₽/сутки

📅 ДАТЫ:
Заезд: {booking.checkin}
Выезд: {booking.checkout}

👤 КЛИЕНТ:
Имя: {booking.guest_name}
Телефон: {booking.guest_phone}
Email: {booking.guest_email or 'Не указан'}

💬 ПОЖЕЛАНИЯ:
{booking.comment or 'Не указаны'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    msg = MIMEMultipart()
    msg['From'] = SMTP_EMAIL
    msg['To'] = ADMIN_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain', 'utf-8'))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"✅ Письмо отправлено на {ADMIN_EMAIL}")
        return True
    except Exception as e:
        print(f"❌ Ошибка отправки письма: {e}")
        return False


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


@app.post("/send-booking")
async def send_booking(booking: BookingRequest):
    print(f"\n📥 Новая заявка от {booking.guest_name}")

    email_sent = send_booking_email(booking)

    if not email_sent:
        return {"success": False, "message": "Не удалось отправить заявку. Попробуйте позже."}

    return {"success": True, "message": "✅ Заявка успешно отправлена!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)