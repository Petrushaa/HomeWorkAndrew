from fastapi import APIRouter

from api.auth import router as auth_router
from api.system import router as system_router
from api.tasks import router as tasks_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(system_router)
api_router.include_router(tasks_router)
