import aiohttp
from fastapi import APIRouter

from app.settings import SETTINGS


router = APIRouter()


@router.get("/companies_info")
async def get_my_companies_info():
    """
    Get the list of companies that have installed the integration

    :return: JSON response with the list of companies
    """
    url = "https://api.yclients.com/api/v1/companies"
    headers = {
        "Authorization": f"Bearer {SETTINGS.PARTNER_TOKEN}, User {SETTINGS.USER_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.yclients.v2+json",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url, params={"my": 1}, headers=headers
        ) as response:  # используем параметр my=1, чтобы смотреть только компании, которые установили интеграцию
            return {"status": response.status, "response": await response.json()}
