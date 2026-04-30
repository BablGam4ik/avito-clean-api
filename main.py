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

    {
        "title": "9-к. квартира, 386 м², 15/15 эт.",
        "price": 390000000,
        "price_raw": "390 000 000 ₽",
        "address": "ул. Викторенко, 11\nАэропорт, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/9-k._kvartira_386_m_1515_et._7795042766?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "4-к. квартира, 227,6 м², 11/14 эт.",
        "price": 695000000,
        "price_raw": "695 000 000 ₽",
        "address": "ул. Усачёва, 15А\nСпортивная, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/4-k._kvartira_2276_m_1114_et._7763889506?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "4-к. квартира, 165 м², 6/11 эт.",
        "price": 260000000,
        "price_raw": "260 000 000 ₽",
        "address": "Ул. Сергея Бондарчука, 6\nМичуринский проспект, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/4-k._kvartira_165_m_611_et._8013974932?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 70 м², 5/5 эт.",
        "price": 150000,
        "price_raw": "150 000 ₽ в месяц",
        "address": "Хорошёвское ш., 13Ак3\nХорошёвская, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_70_m_55_et._8004101006?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "1-к. квартира, 51 м², 8/21 эт.",
        "price": 185000,
        "price_raw": "185 000 ₽ в месяц",
        "address": "Хорошёвское ш., 25Ак2\nХорошёвская, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/1-k._kvartira_51_m_821_et._2371532315?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "5-к. квартира, 137,2 м², 12/22 эт.",
        "price": 77000000,
        "price_raw": "77 000 000 ₽",
        "address": "Волоколамское ш., 71к4\nСпартак, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/5-k._kvartira_1372_m_1222_et._7986420394?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "4-к. квартира, 278 м², 15/18 эт.",
        "price": 125000000,
        "price_raw": "125 000 000 ₽",
        "address": "ул. Расплетина, 14\nОктябрьское поле, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/4-k._kvartira_278_m_1518_et._8034049623?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "Своб. планировка, 48,3 м², 22/34 эт.",
        "price": 29200000,
        "price_raw": "29 200 000 ₽",
        "address": "ул. Архитектора Власова, 71к2\nКалужская, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/svob._planirovka_483_m_2234_et._7989907747?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 58 м², 4/7 эт.",
        "price": 30000000,
        "price_raw": "30 000 000 ₽",
        "address": "Ленинградский пр-т, 33к4\nДинамо, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_58_m_47_et._8066693551?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "4-к. апартаменты, 180 м², 9/9 эт.",
        "price": 85000000,
        "price_raw": "85 000 000 ₽",
        "address": "Ксеньинский пер., 3\nПарк культуры, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/4-k._apartamenty_180_m_99_et._8034017141?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "4-к. квартира, 115 м², 16/18 эт.",
        "price": 260000,
        "price_raw": "260 000 ₽ в месяц",
        "address": "ул. Янковского, 1к3\nАминьевская, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/4-k._kvartira_115_m_1618_et._8024416731?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 63,7 м², 11/15 эт.",
        "price": 26400000,
        "price_raw": "26 400 000 ₽",
        "address": "Погонный пр., 3Ак7\nБелокаменная, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_637_m_1115_et._8010920034?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 44 м², 5/19 эт.",
        "price": 150000,
        "price_raw": "150 000 ₽ в месяц",
        "address": "Малая Почтовая ул., 12\nБауманская, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_44_m_519_et._8126891113?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "1-к. квартира, 34,8 м², 2/16 эт.",
        "price": 65000,
        "price_raw": "65 000 ₽ в месяц",
        "address": "2-й Крестовский пер., 8\nРижская, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/1-k._kvartira_348_m_216_et._8074546760?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 66,4 м², 6/6 эт.",
        "price": 45000000,
        "price_raw": "45 000 000 ₽",
        "address": "Уланский пер., 11А\nСретенский бульвар, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_664_m_66_et._7337803639?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 54 м², 5/16 эт.",
        "price": 138000,
        "price_raw": "138 000 ₽ в месяц",
        "address": "Слесарный пер., 3\nПроспект Мира, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_54_m_516_et._2726099371?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "3-к. квартира, 117 м², 15/26 эт.",
        "price": 250000,
        "price_raw": "250 000 ₽ в месяц",
        "address": "пр. Берёзовой Рощи, 12\nЦСКА, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/3-k._kvartira_117_m_1526_et._8066358688?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 58,1 м², 9/16 эт.",
        "price": 80000,
        "price_raw": "80 000 ₽ в месяц",
        "address": "Ленская ул., 23\nБабушкинская, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_581_m_916_et._8042392154?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 39 м², 8/14 эт.",
        "price": 85000,
        "price_raw": "85 000 ₽ в месяц",
        "address": "Сельскохозяйственная ул., 39\nОтрадное, 16–20 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_39_m_814_et._4577226950?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 58 м², 15/26 эт.",
        "price": 120000,
        "price_raw": "120 000 ₽ в месяц",
        "address": "Красноказарменная ул., 15к2\nАвиамоторная, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_58_m_1526_et._4133646075?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "3-к. квартира, 88 м², 5/8 эт.",
        "price": 220000,
        "price_raw": "220 000 ₽ в месяц",
        "address": "Фрунзенская наб., 32\nФрунзенская, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/3-k._kvartira_88_m_58_et._7925714495?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "4-к. квартира, 127,1 м², 12/65 эт.",
        "price": 950000,
        "price_raw": "950 000 ₽ в месяц",
        "address": "Краснопресненская наб., 14Ак2\nДеловой центр, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/4-k._kvartira_1271_m_1265_et._7251219682?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "3-к. апартаменты, 51,5 м², 11/16 эт.",
        "price": 115000,
        "price_raw": "115 000 ₽ в месяц",
        "address": "Квартал № 2, 5с1\nРумянцево, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/3-k._apartamenty_515_m_1116_et._7822439476?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 63 м², 8/22 эт.",
        "price": 79999,
        "price_raw": "79 999 ₽ в месяц",
        "address": "Ленинский пр-т, 109/1к1\nНоваторская, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_63_m_822_et._8007722709?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 66 м², 10/26 эт.",
        "price": 31900000,
        "price_raw": "31 900 000 ₽",
        "address": "Небесный б-р, 1к1\nСпартак, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_66_m_1026_et._8041297579?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "3-к. квартира, 118 м², 8/14 эт.",
        "price": 290000,
        "price_raw": "290 000 ₽ в месяц",
        "address": "Мытная ул., 7с1\nСерпуховская, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/3-k._kvartira_118_m_814_et._8101589500?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "3-к. квартира, 73 м², 4/5 эт.",
        "price": 30500000,
        "price_raw": "30 500 000 ₽",
        "address": "Прудовой пр., 10\nОстанкино, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/3-k._kvartira_73_m_45_et._7307094669?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 54 м², 8/30 эт.",
        "price": 125000,
        "price_raw": "125 000 ₽ в месяц",
        "address": "Волгоградский пр-т, 32/5к2\nУгрешская, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_54_m_830_et._8096413750?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 58 м², 7/23 эт.",
        "price": 99500,
        "price_raw": "99 500 ₽ в месяц",
        "address": "ул. Лётчика Осканова, 6\nВерхние Лихоборы, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_58_m_723_et._4730849469?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "Квартира-студия, 30 м², 21/21 эт.",
        "price": 78000,
        "price_raw": "78 000 ₽ в месяц",
        "address": "3-я Хорошёвская ул., 17А\nЗорге, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/kvartira-studiya_30_m_2121_et._7370682626?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 47 м², 28/33 эт.",
        "price": 100000,
        "price_raw": "100 000 ₽ в месяц",
        "address": "Амурская ул., 2к1\nЛокомотив, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_47_m_2833_et._8118574624?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 56,2 м², 8/9 эт.",
        "price": 85000,
        "price_raw": "85 000 ₽ в месяц",
        "address": "Шарикоподшипниковская ул., 36/18\nДубровка, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_562_m_89_et._8026200860?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 62,2 м², 11/33 эт.",
        "price": 80000,
        "price_raw": "80 000 ₽ в месяц",
        "address": "Новохохловская ул., 15к1\nНовохохловская, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_622_m_1133_et._8029123379?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "1-к. квартира, 32,1 м², 13/31 эт.",
        "price": 110000,
        "price_raw": "110 000 ₽ в месяц",
        "address": "Дмитровское ш., 75/77\nВерхние Лихоборы, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/1-k._kvartira_321_m_1331_et._8026339990?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 65 м², 7/22 эт.",
        "price": 98000,
        "price_raw": "98 000 ₽ в месяц",
        "address": "ул. Герасима Курина, 18\nСлавянский бульвар, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_65_m_722_et._1245819623?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 58 м², 3/25 эт.",
        "price": 67000,
        "price_raw": "67 000 ₽ в месяц",
        "address": "Покровская ул., 12\nНекрасовка, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_58_m_325_et._8072913353?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "3-к. квартира, 70 м², 17/60 эт.",
        "price": 225000,
        "price_raw": "225 000 ₽ в месяц",
        "address": "Дмитровский пр., 1\nДмитровская, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/3-k._kvartira_70_m_1760_et._8055927615?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "Квартира-студия, 27 м², 25/25 эт.",
        "price": 69000,
        "price_raw": "69 000 ₽ в месяц",
        "address": "Тагильская ул., 2к1\nБульвар Рокоссовского, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/kvartira-studiya_27_m_2525_et._7783229056?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 69,5 м², 16/24 эт.",
        "price": 100000,
        "price_raw": "100 000 ₽ в месяц",
        "address": "1-й Грайвороновский пр., 3\nТекстильщики, 16–20 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_695_m_1624_et._7826226038?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "1-к. квартира, 32,7 м², 1/9 эт.",
        "price": 10950000,
        "price_raw": "10 950 000 ₽",
        "address": "Чертановская ул., 43к2\nПражская, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/1-k._kvartira_327_m_19_et._8096787726?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "1-к. квартира, 33,6 м², 20/30 эт.",
        "price": 87000,
        "price_raw": "87 000 ₽ в месяц",
        "address": "Большая Очаковская ул., 2\nАминьевская, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/1-k._kvartira_336_m_2030_et._7578559170?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "Апартаменты-студия, 18,6 м², 8/8 эт.",
        "price": 59000,
        "price_raw": "59 000 ₽ в месяц",
        "address": "Электрозаводская ул., 14с1\nЭлектрозаводская, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/apartamenty-studiya_186_m_88_et._3462175683?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "Квартира-студия, 19 м², 7/9 эт.",
        "price": 5000000,
        "price_raw": "5 000 000 ₽",
        "address": "Аминьевское ш., 11\nДавыдково, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/kvartira-studiya_19_m_79_et._7744617789?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "Апартаменты-студия, 36,4 м², 1/6 эт.",
        "price": 6419000,
        "price_raw": "6 419 000 ₽",
        "address": "Нижняя Красносельская ул., 45/17\nБауманская, до 5 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/apartamenty-studiya_364_m_16_et._7770651152?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "2-к. квартира, 51,3 м², 6/17 эт.",
        "price": 64000,
        "price_raw": "64 000 ₽ в месяц",
        "address": "Каргопольская ул., 10\nОтрадное, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/2-k._kvartira_513_m_617_et._8034864500?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "Апартаменты-студия, 25 м², 2/5 эт.",
        "price": 40000,
        "price_raw": "40 000 ₽ в месяц",
        "address": "Гостиничная ул., 10к5\nОкружная, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/apartamenty-studiya_25_m_25_et._4254716386?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "1-к. квартира, 32 м², 5/9 эт.",
        "price": 100000,
        "price_raw": "100 000 ₽ в месяц",
        "address": "Новодевичий пр., 10\nСпортивная, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/1-k._kvartira_32_m_59_et._4002944651?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "1-к. квартира, 31 м², 1/9 эт.",
        "price": 50000,
        "price_raw": "50 000 ₽ в месяц",
        "address": "Кустанайская ул., 14к1\nКрасногвардейская, 6–10 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/1-k._kvartira_31_m_19_et._8027803150?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "1-к. квартира, 45 м², 5/5 эт.",
        "price": 55000,
        "price_raw": "55 000 ₽ в месяц",
        "address": "Большая Черёмушкинская ул., 12к1\nКрымская, 11–15 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/1-k._kvartira_45_m_55_et._7774966414?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    },
    {
        "title": "Квартира-студия, 25 м², 14/33 эт.",
        "price": 55000,
        "price_raw": "55 000 ₽ в месяц",
        "address": "рп. Новоивановское, Можайское ш., 54\nНемчиновка, 16–20 мин.",
        "link": "https://www.avito.ru/moskva/kvartiry/kvartira-studiya_25_m_1433_et._7253220149?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJRZ2R2eTRHVWl0QWptQzN3Ijt9IHL33z8AAAA"
    }
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