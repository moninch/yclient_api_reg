from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

router = APIRouter()


@router.get("/check_integration")
async def check_integration(url: str):
    """
    Check if a company has installed the integration
    :param url: Integration link
    :return: JSON response with the company status
    """
    branch_id = url.split("/company/")[1].split("/")[0]
    # Проверить наличие branch_id в вашей базе данных
    # Пример: поиск в MongoDB
    # company = companies_collection.find_one({"id": int(branch_id)})
    company = None  # Замените на реальную логику
    if company:
        return JSONResponse(content={"status": "integrated", "company": company})
    else:
        raise HTTPException(status_code=404, detail="Company not found.")
