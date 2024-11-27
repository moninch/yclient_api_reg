from os import environ, getenv
from pydantic import BaseModel, SecretStr
from dotenv import load_dotenv

load_dotenv(".env")


class Settings(BaseModel):
    LOGGING_LEVEL: str

    API_PORT: int
    API_HOST: str

    MONGODB_URL: SecretStr
    MONGODB_DB: SecretStr

    PARTNER_TOKEN: SecretStr
    USER_TOKEN: SecretStr


SETTINGS = Settings(**environ)
