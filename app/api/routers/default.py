from typing import Optional
from fastapi import APIRouter
import aiohttp
from starlette.responses import JSONResponse
from app.settings import SETTINGS

router = APIRouter()


@router.get("/")
async def root():
    return JSONResponse(content={"message": "Hello World"})


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


# https://n1290414.yclients.com/company/1177126/personal/select-time?o=m3570915s17612273d2425111900
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
