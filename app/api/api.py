from fastapi import APIRouter

from .controller.v1 import v1

router = APIRouter(
    prefix="/api"
)

router.include_router(v1.router)


#
# dir_path = "app/api/routes"
#
# files_dir = [
#     ".routes."+f for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f)) and f != '__pycache__'
# ]
#
# modules = map(__import__, files_dir)
# for module in modules:
#     print(module.name)
