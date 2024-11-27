import aiohttp
from fastapi import APIRouter

from app.settings import SETTINGS


router = APIRouter()


@router.get("/book_times")
async def get_book_times(
    company_id: int = 1177126,  # ID of the company
    staff_id: int = 3570915,  # ID of the staff member
):
    """
    Get the list of available booking times for the specified company and staff member

    :param company_id: ID of the company
    :param staff_id: ID of the staff member
    :return: JSON response with the list of available booking times
    """
    url = f"https://api.yclients.com/api/v1/book_staff_seances/{company_id}/{staff_id}/"
    headers = {
        "Authorization": f"Bearer {SETTINGS.PARTNER_TOKEN}, User {SETTINGS.USER_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.yclients.v2+json",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return {"status": response.status, "response": await response.json()}


@router.post("/book_record")
async def book_record(company_id: int = 1177126):  # ID of the company
    url = f"https://api.yclients.com/api/v1/book_record/{company_id}"
    headers = {
        "Authorization": f"Bearer {SETTINGS.PARTNER_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.yclients.v2+json",
    }
    data = {
        "phone": "79000000000",
        "fullname": "John Doe",
        "email": "sosa@mail.ru",
        "appointments": [
            {
                "id": 176122723433,
                "staff_id": 0,
                "services": [17612273],
                "datetime": "2024-11-25T19:03:00+03:00",
            }
        ],
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            return {"status": response.status, "response": await response.json()}
