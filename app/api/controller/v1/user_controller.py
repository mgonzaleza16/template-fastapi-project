from typing import Annotated, Final

from fastapi import APIRouter, Query
from fastapi.responses import ORJSONResponse

from ...dto.user_dto import UserDto
from ...service.impl.user_service_impl import UserServiceImpl
from ...service.user_service import UserService

router = APIRouter(prefix="/users")

router.tags = ["User"]

_user_service: Final[UserService] = UserServiceImpl()


@router.get("/all", name="Get all users", response_class=ORJSONResponse, response_model=list[UserDto])
async def get_all_users():
    return await _user_service.all()


@router.get("/", name="Find by email", response_class=ORJSONResponse, response_model=UserDto)
async def find_by_email(email: Annotated[str, Query(description="the email address of the user")]):
    return await _user_service.find_by_email(email)
