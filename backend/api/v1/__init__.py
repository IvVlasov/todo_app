from fastapi import APIRouter

from backend.api.v1.auth.routes import router as auth_router
from backend.api.v1.tasks.routes import router as tasks_router
from backend.api.v1.user.routes import router as user_router


router = APIRouter(prefix="/v1")

router.include_router(user_router)
router.include_router(auth_router)
router.include_router(tasks_router)
