import aiohttp
from fastapi import APIRouter, HTTPException, requests
from pymongo import MongoClient

from app.settings import SETTINGS
from app.__main__ import MongoDB

router = APIRouter()


@router.get("/companies_info")
async def get_my_companies_info():
    """
    Обновить список компаний, установивших интеграцию.
    """
    url = "https://api.yclients.com/api/v1/companies"
    headers = {
        "Authorization": f"Bearer {SETTINGS.PARTNER_TOKEN}, User {SETTINGS.USER_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.yclients.v2+json",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params={"my": 1}, headers=headers) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=response.status, detail="Ошибка при получении компаний"
                )

            companies = (await response.json()).get("data", [])
            for company in companies:
                company_data = {
                    "branch_id": company["id"],
                    "title": company["title"],
                    "email": company.get("email", ""),
                    "city": company.get("city", ""),
                }
                MongoDB.db.get_collection("companies").update_one(
                    {"branch_id": company_data["branch_id"]},
                    {"$set": company_data},
                    upsert=True,
                )

            return {"message": "Компании обновлены", "count": len(companies)}
