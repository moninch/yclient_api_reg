from typing import Optional
from fastapi import APIRouter
import aiohttp
from starlette.responses import JSONResponse
from app.settings import SETTINGS

# https://n1290414.yclients.com/company/1177126/personal/select-time?o=m3570915s17612273d2425111900
router = APIRouter()


@router.get("/")
async def root():
    return JSONResponse(content={"message": "Hello World"})
