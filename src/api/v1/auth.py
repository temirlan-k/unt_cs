from fastapi import APIRouter, Depends

from src.core.auth_middleware import get_current_user
from src.schemas.req.user import UserCreateReq, UserLoginReq
from src.services.auth import AuthService

auth_router = APIRouter()


@auth_router.post("/login")
async def login(req: UserLoginReq, auth_service: AuthService = Depends(AuthService)):
    return await auth_service.login(req)


@auth_router.post("/register")
async def register(
    req: UserCreateReq, auth_service: AuthService = Depends(AuthService)
):
    return await auth_service.create_user(req)
