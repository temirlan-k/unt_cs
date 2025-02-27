from fastapi import APIRouter, Depends

from src.core.auth_middleware import get_current_user
from src.schemas.req.profile import  UserProfileUpdateReq
from src.services.profile import ProfileService

profile_router = APIRouter()


@profile_router.patch("/update")
async def update_profile(
    req: UserProfileUpdateReq,
    token: dict = Depends(get_current_user),
    profile_service: ProfileService = Depends(ProfileService),
):

    return await profile_service.update_profile(token.get("sub"), req)


@profile_router.get("/me")
async def me(
    token: dict = Depends(get_current_user),
    profile_service: ProfileService = Depends(ProfileService),
):
    return await profile_service.get_user_by_id(token.get("sub"))
