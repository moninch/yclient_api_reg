from typing import Optional
from fastapi import APIRouter
import aiohttp
from starlette.responses import JSONResponse
from app.settings import SETTINGS

router = APIRouter()


@router.get("/")
async def root():
    return JSONResponse(content={"message": "Hello World"})
