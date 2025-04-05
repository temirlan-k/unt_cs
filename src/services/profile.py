import os
import shutil
import logging
from beanie import Link, PydanticObjectId
from bson import ObjectId
from fastapi import File, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse

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

    async def get_leaderboard(self, skip: int = 0, limit: int = 10):
        """Возвращает топ пользователей по total_score с поддержкой пагинации"""
        users = await User.find().sort("-total_score").skip(skip).limit(limit).to_list()
        total_users = await User.count()  # Общее количество пользователей
        return {'users': users, "users_count": total_users}

    async def get_user_rank(self, user_id: str):
        """Возвращает место текущего пользователя в лидерборде и его total_score"""
        user = await User.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        rank = await User.find(User.total_score > user.total_score).count() + 1
        total_users = await User.count()

        return {"rank": rank, "total_score": user.total_score, "users_count": total_users}

    async def update_profile_photo(self, user_id: str, file: UploadFile):
        """Обновляет фото пользователя, удаляя старое"""
        user = await User.get(user_id)
        UPLOAD_DIR = "uploads"

        if not user:
            return {"error": "User not found"}

        # Удаляем старый файл, если он есть
        if user.profile_photo:
            old_file_path = os.path.abspath(user.profile_photo)
            if os.path.exists(old_file_path):
                os.remove(old_file_path)  # Удаление старого файла

        # Определяем новое имя файла с оригинальным расширением
        file_extension = file.filename.split(".")[-1]  # Например, "jpg" или "png"
        new_file_name = f"{user_id}.{file_extension}"
        new_file_path = os.path.join(UPLOAD_DIR, new_file_name)

        # Сохраняем новый файл
        with open(new_file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Обновляем запись в базе
        user.profile_photo = new_file_path
        await user.save()

        return {"message": "Profile photo updated successfully", "photo_url": user.profile_photo}    

    async def get_profile_photo(self, user_id: str):
        user = await User.get(user_id)
        if not user or not user.profile_photo:
            return {"error": "Photo not found"}
        UPLOAD_DIR = "uploads"
        os.makedirs(UPLOAD_DIR, exist_ok=True)  
        file_path = user.profile_photo
        print(file_path)
        logging.debug(f"File Path:{file_path}")
        if file_path is None:
            raise HTTPException(status_code=404,detail='You dont have profile photo')

        return FileResponse(file_path,    headers={
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0",
    })