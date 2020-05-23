from fastapi import APIRouter

from app.service_layer.api.api_v1.endpoints import users, wallets, transfers

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(wallets.router, prefix="/wallets", tags=["wallets"])
api_router.include_router(transfers.router, prefix="/transfers", tags=["transfers"])
