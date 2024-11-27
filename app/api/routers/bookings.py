import aiohttp
from fastapi import APIRouter, HTTPException
import random
from app.settings import SETTINGS

router = APIRouter()


@router.get("/available_times")
async def fetch_available_times(company_id=1177126, staff_id=3570847):
    """
    Получить список доступных временных слотов
    """
    url = f"https://api.yclients.com/api/v1/book_staff_seances/{company_id}/{staff_id}/"
    headers = {
        "Authorization": f"Bearer {SETTINGS.PARTNER_TOKEN}, User {SETTINGS.USER_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.yclients.v2+json",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=response.status, detail="Ошибка при получении времени"
                )
            return await response.json()


@router.get("/fetch_services")
async def fetch_services(
    company_id: int = 1177126,
    service_id: int = None,
    staff_id: int = None,
    category_id: int = None,
):
    """
    Получить список услуг компании или конкретную услугу с фильтрацией.
    """
    url = f"https://api.yclients.com/api/v1/company/{company_id}/services"
    if service_id:
        url += f"/{service_id}"

    params = {}
    if staff_id:
        params["staff_id"] = staff_id
    if category_id:
        params["category_id"] = category_id

    headers = {
        "Authorization": f"Bearer {SETTINGS.PARTNER_TOKEN}, User {SETTINGS.USER_TOKEN}",
        "Accept": "application/vnd.yclients.v2+json",
        "Content-Type": "application/json",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=response.status,
                    detail="Ошибка при получении услуг",
                )
            response_data = await response.json()

            # Преобразование данных под упрощённый вид
            services = [
                {
                    "id": service.get("id"),
                    "title": service.get("title"),
                    "duration": service.get("duration"),
                    "staff": [
                        {
                            "id": staff["id"],
                            "name": staff["name"],
                        }
                        for staff in service.get("staff", [])
                    ],
                }
                for service in response_data.get("data", [])
            ]
            return {"success": True, "services": services}


@router.post("/book")
async def book_appointment(
    url: str = "https://n1290414.yclients.com/company/1177126/create-record/record?o=m3570847s17612273d2427111500",
    phone: str = "79518374484",
    fullname: str = "sosa",
    email: str = "bebra@mail.ru",
    datetime: str = "2024-11-27T17:30:00+03:00",
):
    """
    Создать запись по предоставленному URL
    """
    try:
        company_id = int(url.split("/company/")[1].split("/")[0])
        staff_id = int(url.split("o=m")[1].split("s")[0])
        service = int(url.split("o=m")[1].split("s")[1].split("d")[0])
    except (IndexError, ValueError):
        raise HTTPException(status_code=400, detail="Неверный формат URL")

    # Проверить доступные услуги
    # services_data = await fetch_services(company_id=company_id, staff_id=staff_id)
    # services = services_data.get("services", [])
    # if not services:
    #     raise HTTPException(status_code=400, detail="Услуги не найдены")

    # Проверить доступное время
    # available_times = await fetch_available_times(company_id, staff_id)
    # if datetime not in [
    #     slot["datetime"] for slot in available_times.get("data", {}).get("seances", [])
    # ]:
    #     raise HTTPException(status_code=400, detail="Время недоступно")

    # Создать запись
    book_url = f"https://api.yclients.com/api/v1/book_record/{company_id}"
    headers = {
        "Authorization": f"Bearer {SETTINGS.PARTNER_TOKEN}, User {SETTINGS.USER_TOKEN}",
        "Accept": "application/vnd.yclients.v2+json",
        "Content-Type": "application/json",
    }
    data = {
        "phone": phone,
        "fullname": fullname,
        "email": email,
        "appointments": [
            {
                "id": random.randint(100000, 999999),
                "staff_id": staff_id,
                "services": [service],
                "datetime": datetime,
            }
        ],
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(book_url, json=data, headers=headers) as response:
            if response.status != 200 and response.status != 201:
                raise HTTPException(
                    status_code=response.status, detail="Ошибка при создании записи"
                )
            return await response.json()
