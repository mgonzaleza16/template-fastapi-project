from fastapi import APIRouter

from . import chat_bot_activity_controller, user_controller

router = APIRouter(
    prefix="/1.0"
)

router.include_router(user_controller.router)
router.include_router(chat_bot_activity_controller.router)
