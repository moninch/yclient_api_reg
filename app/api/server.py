from fastapi import FastAPI
from app.api.routers.default import router as default_router
from app.settings import SETTINGS
from app.utils.mongodb import MongoDB

app = FastAPI()

app.include_router(default_router)


@app.on_event("startup")
async def app_startup():

    MongoDB.setup(
        SETTINGS.MONGODB_URL.get_secret_value(), SETTINGS.MONGODB_DB.get_secret_value()
    )
