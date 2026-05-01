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

# ===== НАСТРОЙКИ ДЛЯ ОТПРАВКИ ПИСЕМ (GMAIL) =====
# ВНИМАНИЕ: Вместо "ВАШ_ПАРОЛЬ_ПРИЛОЖЕНИЯ" вставьте 16-значный пароль из Google
SMTP_SERVER = "smtp.beget.com"
SMTP_PORT = 465
SMTP_EMAIL = "v9504205"  # Логин от панели Beget + @ваш_домен
SMTP_PASSWORD = "jYZ5VOv9XV1j"       # Пароль от панели управления Beget
ADMIN_EMAIL = "korpacevegor@gmail.com"         # Куда приходя


# ===============================================

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
# ВАШИ 50 КВАРТИР (сокращено, добавьте свои)
# ============================================
REAL_APARTMENTS = [
    {
        "title": "Квартира",
        "price": 600000,
        "price_raw": "600 000 ₽ в месяц",
        "address": "Береговая ул., 4к3\nБалтийская, 21–30 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/6-k._kvartira_270_m_16_et._8027548088?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": "https://70.img.avito.st/image/1/1.eISi-ba-1G20WXZs3ogU5Z9Z1msQTtBtECm1Zxz61c8XWtY.ZHUH_YfvzmRxR9YNwmwrDiFYutMcjkxs4C5Y4RM--YM"
    },
    {
        "title": "Квартира",
        "price": 2497000,
        "price_raw": "2 497 000 ₽",
        "address": "Сходненская ул., 22А\nСходненская, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/apartamenty-studiya_118_m_44_et._7953229086?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": "https://30.img.avito.st/image/1/1.hLiB4ba-KFGXQYpQhefnwbJBKlczVixRMzFJWz_iKfM0Qio.7O_8TrBc-xuY2pyQ3795OxFp9POgG8n6p0UOKa6YxUM?cqp=2.U5qO8d4CHIiNW2QBtZw-uX6ewmB-LGaDE3-rkUTl5s3E6YkLER2eWpxBXXm-uAtjIUjyebQ7nSoGxTRjJ3W_erzY_jCAaA=="
    },
    {
        "title": "Квартира",
        "price": 77000,
        "price_raw": "77 000 ₽ в месяц",
        "address": "Кавказский б-р, 51к1\nКантемировская, 16–20 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_36_m_3033_et._8075134262?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": "https://00.img.avito.st/image/1/1.Y3vgSLa-z5L26G2TqhVgKtzozZRS_8uSUpiumF5LzjBV680.tS9jG-NGitfCqXP6WmjNP9l1Rzql4ATUM_Q9ubkCyLc?cqp=2.U5qO8d4CHIiNW2QBtZw-uX6ewmB-LGaDE3-rkUTl5s3E6YkLER2eWpxBXXm-uAtjIUjyebQ7nSoGxTRjJ3W_erzY_jCAaA=="
    },
    {
        "title": "Квартира",
        "price": 100000,
        "price_raw": "100 000 ₽ в месяц",
        "address": "1-я Тверская-Ямская ул., 28\nБелорусская, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_62_m_210_et._8027852050?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": "https://30.img.avito.st/image/1/1.5Br2tba-SPPgFerysvaDe8sVSvVEAkzzRGUp-Ui2SVFDFko.KrpQE9Ir9R2al1ofM7xxXiJmdnf_6uTQe2iWZpH5cks?cqp=2.U5qO8d4CHIiNW2QBtZw-uX6ewmB-LGaDE3-rkUTl5s3E6YkLER2eWpxBXXm-uAtjIUjyebQ7nSoGxTRjJ3W_erzY_jCAaA=="
    },
    {
        "title": "Квартира",
        "price": 145000,
        "price_raw": "145 000 ₽ в месяц",
        "address": "Волоколамское ш., 95/2к5\nТрикотажная, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_569_m_828_et._7416564460?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": "https://90.img.avito.st/image/1/1.V3Pz3La--5rlfFmb0YFRK459-ZxBa_-aQQyakE3f-jhGf_k.3G6rAscAE-E5aEpc-COagLPNgh3gP1oOnm3FdiLo5ls"
    },
    {
        "title": "Квартира",
        "price": 350000,
        "price_raw": "350 000 ₽ в месяц",
        "address": "Большой Толмачёвский пер., 4с1\nТретьяковская, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/3-k._kvartira_121_m_28_et._8075199619?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": "https://20.img.avito.st/image/1/1.8910S7a-XzRi6_01HhiumEjrXTLG_Fs0xps-PspIXpbB6F0.X_VyUdLuRUmdmw_t7gI8QMG6CJG_KM-A_P6mtr2OA6g?cqp=2.U5qO8d4CHIiNW2QBtZw-uX6ewmB-LGaDE3-rkUTl5s3E6YkLER2eWpxBXXm-uAtjIUjyebQ7nSoGxTRjJ3W_erzY_jCAaA=="
    },
    {
        "title": "Квартира",
        "price": 38000,
        "price_raw": "38 000 ₽ в месяц",
        "address": "Изюмская ул., 49к4\nБутово, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/1-k._kvartira_40_m_612_et._7996732014?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 23800000,
        "price_raw": "23 800 000 ₽",
        "address": "Севастопольский пр-т, 22А\nНагорная, 16–20 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._apartamenty_495_m_2242_et._8016765632?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 285000,
        "price_raw": "285 000 ₽ в месяц",
        "address": "Чапаевский пер., 3\nАэропорт, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/4-k._kvartira_133_m_512_et._3683869554?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 89000000,
        "price_raw": "89 000 000 ₽",
        "address": "Ленинградский пр-т, 29к4\nДинамо, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/4-k._kvartira_99_m_59_et._7993962240?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 12500000,
        "price_raw": "12 500 000 ₽",
        "address": "Зеленоградская ул., 31к5\nХоврино, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_383_m_212_et._8028334818?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 139900,
        "price_raw": "139 900 ₽ в месяц",
        "address": "Шмитовский пр., 39к6\nШелепиха, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_46_m_3052_et._7809165172?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 13500000,
        "price_raw": "13 500 000 ₽",
        "address": "Студёный пр., 14\nМедведково, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/1-k._kvartira_375_m_517_et._7996078482?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 250000,
        "price_raw": "250 000 ₽ в месяц",
        "address": "ул. Янковского, 1к3\nАминьевская, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/4-k._kvartira_115_m_1618_et._8024416731?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": "https://50.img.avito.st/image/1/1.MzMvVra5idoZ9x3aRRIibRz2ndyd0x3amf-_2Jn1idg.xvWU4vaL-CBLuX6SbAHhDLqSL3GfjroCzxiMdRkmZQo"
    },
    {
        "title": "Квартира",
        "price": 75000,
        "price_raw": "75 000 ₽ в месяц",
        "address": "Амурская ул., 2к1\nЛокомотив, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/1-k._kvartira_32_m_1728_et._8027539341?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 200000,
        "price_raw": "200 000 ₽ в месяц",
        "address": "Багратионовский пр., 5Ак1\nФили, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/3-k._kvartira_66_m_4141_et._7719867090?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 17400000,
        "price_raw": "17 400 000 ₽",
        "address": "ул. Яблочкова, 21\nТимирязевская, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_38_m_312_et._8034739164?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 49900000,
        "price_raw": "49 900 000 ₽",
        "address": "Ленинградский пр-т, 29к2\nДинамо, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/svob._planirovka_854_m_621_et._7972199984?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 79000,
        "price_raw": "79 000 ₽ в месяц",
        "address": "Энергетическая ул., 20\nАвиамоторная, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_55_m_48_et._7978947430?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 181000,
        "price_raw": "181 000 ₽ в месяц",
        "address": "Ломоносовский пр-т, 41к1\nЛомоносовский проспект, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/4-k._kvartira_1354_m_1924_et._7902168024?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 75000,
        "price_raw": "75 000 ₽ в месяц",
        "address": "Грайвороновская ул., 4с2\nТекстильщики, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/apartamenty-studiya_33_m_22_et._8028513803?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 72000,
        "price_raw": "72 000 ₽ в месяц",
        "address": "Варшавское ш., 170Ек10\nЛесопарковая, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/1-k._kvartira_38_m_1719_et._7727215635?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 88000,
        "price_raw": "88 000 ₽ в месяц",
        "address": "ул. Василия Ланового, 1к2\nАминьевская, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/1-k._kvartira_28_m_1843_et._7851913754?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 34999999,
        "price_raw": "34 999 999 ₽",
        "address": "Потешная ул., 2\nПреображенская площадь, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/4-k._kvartira_961_m_18_et._8043283978?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": "https://90.img.avito.st/image/1/1.KwVj9ba6kexVVAXsOfl3CrxWgerz1ofu33SF7tVChQ.z50hT1kC-8DhsaRqNP1ULzIA-V5Ah6fldUka2E4_pOM"
    },
    {
        "title": "Квартира",
        "price": 250000,
        "price_raw": "250 000 ₽ в месяц",
        "address": "Ружейный пер., 3\nСмоленская, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_62_m_1516_et._8089692998?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 15900000,
        "price_raw": "15 900 000 ₽",
        "address": "Ангарская ул., 51к2\nЯхромская, 16–20 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_511_m_217_et._7910660120?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": "https://40.img.avito.st/image/1/1.PovnDLa5hGLRrRBil2RUquGukGRViRBiUaWyYFGvhGA.2cDiAKFlV4gs-qxfQlBVrptr97SYM2kttjgBqslG008"
    },
    {
        "title": "Квартира",
        "price": 74999,
        "price_raw": "74 999 ₽ в месяц",
        "address": "пр. Шокальского, 41\nМедведково, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_68_m_314_et._7635223224?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 115000,
        "price_raw": "115 000 ₽ в месяц",
        "address": "Трифоновская ул., 57к1\nРижская, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_443_m_29_et._7989378027?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 80000,
        "price_raw": "80 000 ₽ в месяц",
        "address": "ул. Газопровод, 13к1\nКрасный Строитель, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_54_m_517_et._3154504365?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 80000,
        "price_raw": "80 000 ₽ в месяц",
        "address": "Сиреневый б-р, 43А\nЩёлковская, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/3-k._kvartira_65_m_39_et._7980125584?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 45000,
        "price_raw": "45 000 ₽ в месяц",
        "address": "пр-т Куприна, 7к3\nПотапово, 21–30 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/kvartira-studiya_23_m_1017_et._7998757889?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 95000,
        "price_raw": "95 000 ₽ в месяц",
        "address": "Херсонская ул., 43\nЗюзино, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_55_m_816_et._7944442631?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 60000,
        "price_raw": "60 000 ₽ в месяц",
        "address": "Коровинское ш., 4А\nСелигерская, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/1-k._kvartira_46_m_2024_et._4070430580?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 100000,
        "price_raw": "100 000 ₽ в месяц",
        "address": "Часовая ул., 21А\nКрасный Балтиец, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_44_m_45_et._8095182080?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 29000000,
        "price_raw": "29 000 000 ₽",
        "address": "Шелепихинская наб., 34к3\nШелепиха, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_456_m_1134_et._7569931667?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": "https://10.img.avito.st/image/1/1.myQGbLa5Ic0wzbXNPCKQZ2PNNcu06bXNsMUXz7DPIc8.ItCJzOFm7W79v0HQaVTap9TIOSTCmNo-ImEbAF7aoJg?cqp=2.pGdjs5fBvl5-fB-fm84xxYDAkt8GM2Wgr1fOyxua9Q=="
    },
    {
        "title": "Квартира",
        "price": 130000,
        "price_raw": "130 000 ₽ в месяц",
        "address": "Волгоградский пр-т, 32/5к3\nВолгоградский проспект, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_39_m_1330_et._8096685691?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 85000,
        "price_raw": "85 000 ₽ в месяц",
        "address": "1-я Магистральная ул., 25\nХорошёвская, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_36_m_522_et._7975633227?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 75000,
        "price_raw": "75 000 ₽ в месяц",
        "address": "ул. Василисы Кожиной, 16к2\nФилёвский парк, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_433_m_25_et._7966083719?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 75000,
        "price_raw": "75 000 ₽ в месяц",
        "address": "Большая Черкизовская ул., 9к1\nПреображенская площадь, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/kvartira-studiya_31_m_58_et._7376131550?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 60000,
        "price_raw": "60 000 ₽ в месяц",
        "address": "Кировоградская ул., 22\nПражская, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_582_m_922_et._8075353839?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 45000,
        "price_raw": "45 000 ₽ в месяц",
        "address": "Байкальская ул., 15\nЩёлковская, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/kvartira-studiya_28_m_49_et._8118861088?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 90000,
        "price_raw": "90 000 ₽ в месяц",
        "address": "Нагатинская наб., 10А\nНагатинская, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/1-k._kvartira_38_m_1026_et._7975827627?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 11900000,
        "price_raw": "11 900 000 ₽",
        "address": "Новгородская ул., 7\nАлтуфьево, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/1-k._kvartira_369_m_516_et._8058622493?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 19500000,
        "price_raw": "19 500 000 ₽",
        "address": "Скобелевская ул., 3к1\nУлица Скобелевская, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_537_m_1316_et._8027781346?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 29000,
        "price_raw": "29 000 ₽ в месяц",
        "address": "Новороссийская ул., 7\nЛюблино, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/kvartira-studiya_14_m_15_et._8017278689?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 149000000,
        "price_raw": "149 000 000 ₽",
        "address": "Кудринская пл., 1\nБаррикадная, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/3-k._kvartira_136_m_1031_et._8041650760?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": "https://10.img.avito.st/image/1/1.fuIXcba6xAsh0FALZwAJ28nS1A2HUtIJq_DQCaHG0A.k0yL59xGG8Ros-F1R-rJYBBuyS28SFZILWAHGDWvZGg?cqp=2.pGdjs5fBvl5-fB-fm84xxYDAkt8GM2Wgr1fOyxua9Q=="
    },
    {
        "title": "Квартира",
        "price": 21000000,
        "price_raw": "21 000 000 ₽",
        "address": "ЖК «Скай Гарден» \nПроезд Строительный, д. 9, корпус 1\nТушинская, 16–20 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_772_m_444_et._7536247809?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 90000,
        "price_raw": "90 000 ₽ в месяц",
        "address": "Волгоградский пр-т, 32/3к3\nУгрешская, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/1-k._kvartira_37_m_1032_et._7972135234?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 60000,
        "price_raw": "60 000 ₽ в месяц",
        "address": "Федеративный пр-т, 30Ак2\nНовогиреево, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_469_m_712_et._8075145610?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    },
    {
        "title": "Квартира",
        "price": 170000,
        "price_raw": "170 000 ₽ в месяц",
        "address": "4-й Верхний Михайловский пр., 1\nШаболовская, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/3-k._apartamenty_80_m_813_et._7819566477?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJTTnpUQ0JIY0dZb1NIbkxhIjt9RMsyOz8AAAA",
        "img": ""
    }
]


def get_city_from_address(address: str) -> str:
    return "москва"


APARTMENTS_BY_CITY = {"москва": REAL_APARTMENTS}

print(f"📊 Загружено квартир: {len(REAL_APARTMENTS)}")
print(f"🏙️ Города: {list(APARTMENTS_BY_CITY.keys())}")


def send_booking_email(booking: BookingRequest):
    """Функция для отправки письма через Gmail"""
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

    # Если клиент указал email, отправим копию ему
    if booking.guest_email:
        msg['Cc'] = booking.guest_email

    try:
        # Для порта 587 используем starttls()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Включаем шифрование
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"✅ Письмо отправлено на {ADMIN_EMAIL}")
        if booking.guest_email:
            print(f"📧 Копия отправлена клиенту на {booking.guest_email}")
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