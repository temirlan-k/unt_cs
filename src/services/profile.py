from beanie import Link, PydanticObjectId
from bson import ObjectId
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from src.helpers.jwt_handler import JWT
from src.helpers.password import PasswordHandler
from src.models.user import  User
from src.schemas.req.profile import  UserProfileUpdateReq
from src.schemas.req.user import UserCreateReq, UserLoginReq


class ProfileService:

    async def get_user_by_id(self, user_id: str):
        user = await User.find_one(User.id == PydanticObjectId(user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "id": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "score":user.total_score,
            "role":user.role
        }

    async def update_profile(self, user_id: str, profile_data: UserProfileUpdateReq):
        user = await User.find_one(User.id == PydanticObjectId(user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if profile_data.first_name is not None:
            user.first_name = profile_data.first_name
        if profile_data.last_name is not None:
            user.last_name = profile_data.last_name
        if profile_data.email is not None:
            user.email = profile_data.email
        if profile_data.password is not None:
            user.password = PasswordHandler.hash(profile_data.password)

        await user.save()
        return user


    async def get_leaderboard(skip: int = 0, limit: int = 10):
        """Возвращает топ пользователей по total_score с поддержкой пагинации"""
        users = await User.find().sort("-total_score").skip(skip).limit(limit).to_list()
        return users
        