from fastapi import APIRouter

from app.api.routes import items, login, users, utils, labs, borrow

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/labs", tags=["items"])
api_router.include_router(labs.router, prefix="/labs", tags=["labs"])
api_router.include_router(borrow.router, prefix="/labs", tags=["borrow"])
