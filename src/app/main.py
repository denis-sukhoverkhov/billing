from fastapi import FastAPI

from app.service_layer.api.api_v1.router import api_router
from app.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
)
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
