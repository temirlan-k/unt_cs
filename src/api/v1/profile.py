from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, File, UploadFile

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


@profile_router.get('/leaderboard')
async def get_leaderboard(
    skip: int = 0, limit: int = 10,
    profile_service: ProfileService = Depends(ProfileService),
):
    return await profile_service.get_leaderboard(skip,limit)

@profile_router.get("/leaderboard/me", )
async def get_user_rank(    
    token: dict = Depends(get_current_user),
    profile_service: ProfileService = Depends(ProfileService),
):
    """Возвращает место текущего пользователя в лидерборде и его total_score"""
    return await profile_service.get_user_rank((token.get('sub')))


@profile_router.patch("/upload-profile-photo/", )
async def upload_profile_photo(    
    token: dict = Depends(get_current_user),
    file: UploadFile = File(...),
    profile_service: ProfileService = Depends(ProfileService),
):
    """Возвращает место текущего пользователя в лидерборде и его total_score"""
    return await profile_service.update_profile_photo((token.get('sub')),file)

@profile_router.get("/profile-photo/")
async def get_profile_photo(    
    token: dict = Depends(get_current_user),
    profile_service: ProfileService = Depends(ProfileService),
):
    return await profile_service.get_profile_photo((token.get('sub')),)
