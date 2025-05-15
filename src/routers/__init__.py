from fastapi import APIRouter

from .chat import router as chat_router
from .ws import router as ws_router
from .auth import router as auth_router
from .history import router as history_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(chat_router)
router.include_router(history_router)
router.include_router(ws_router)
