from typing import Annotated, Final

from fastapi import APIRouter, Depends, Path

from ...depend.connection_depend import ConnectionDepend
from ...service.chat_bot_activity_service import ChatBotActivityService
from ...service.impl.chat_bot_activity_service_impl import ChatBotActivityServiceImpl

router = APIRouter(prefix="/chat-bot-activity")

router.tags = ["Chat Bot Activity"]

_chat_bot_activity_service: Final[ChatBotActivityService] = ChatBotActivityServiceImpl()


@router.get("/all", name="Get all Activities")
async def get_all_activities(worker: Annotated[str, Depends(ConnectionDepend.create_connection)]):
    return await _chat_bot_activity_service.all(worker)


@router.get("/{task_code}", name="Find by task_code")
async def find_by_email(worker: Annotated[str, Depends(ConnectionDepend.create_connection)],
                        task_code: Annotated[str, Path(description="the task code to find")]):
    return await _chat_bot_activity_service.find_by_task_code(worker, task_code)
