from fastapi import FastAPI

from app.api.api_v1.router import api_router
from app.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)

import logging

logging.basicConfig(filename='db.log')
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
