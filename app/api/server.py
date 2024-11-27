from fastapi import FastAPI
from app.api.routers.default import router as default_router
from app.api.routers.companies import router as companies_router
from app.api.routers.bookings import router as bookings_router
from app.api.routers.integration import router as integration_router
from app.settings import SETTINGS
from app.utils.mongodb import MongoDB

app = FastAPI()

app.include_router(default_router, prefix="/api/v1", tags=["Default"])
app.include_router(companies_router, prefix="/api/v1/companies", tags=["Companies"])
app.include_router(bookings_router, prefix="/api/v1/bookings", tags=["Bookings"])
app.include_router(
    integration_router, prefix="/api/v1/integration", tags=["Integration"]
)


@app.on_event("startup")
async def app_startup():

    MongoDB.setup(
        SETTINGS.MONGODB_URL.get_secret_value(), SETTINGS.MONGODB_DB.get_secret_value()
    )
