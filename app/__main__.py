import asyncio
import uvicorn
from app.settings import SETTINGS


async def main():
    uvicorn.run(
        app="app.api.server:app",
        host=SETTINGS.API_HOST,
        port=SETTINGS.API_PORT,
        log_level=SETTINGS.LOGGING_LEVEL.lower(),
        reload=True,
        reload_includes=["app"],
    )


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    loop.run_forever()
