from fastapi import APIRouter, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from app.__main__ import MongoDB

router = APIRouter()


# https://n1290414.yclients.com/company/1177126/personal/select-time?o=m3570915s17612273d2425111900
@router.get("/check_integration")
async def check_integration(url: str = Query(..., description="Ссылка клиента")):
    """
    Проверить наличие компании в базе по предоставленному URL.
    """
    try:
        # Извлекаем branch_id из URL
        branch_id = int(url.split("/company/")[1].split("/")[0])
    except (IndexError, ValueError):
        raise HTTPException(status_code=400, detail="Неверный формат URL")

    company = await MongoDB.db.get_collection("companies").find_one(
        {"branch_id": branch_id}
    )
    if company:
        company["_id"] = str(company["_id"])
        return jsonable_encoder({"status": "integrated", "company": company})
    else:
        raise HTTPException(status_code=404, detail="Компания не найдена")
