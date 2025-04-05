from datetime import datetime
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
            "role":user.role,
            "profile_photo":user.profile_photo if user.profile_photo else None
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
        # Ensure upload directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        if not user:
            return {"error": "User not found"}
        
        # Удаляем старый файл, если он есть
        if user.profile_photo and os.path.exists(user.profile_photo):
            try:
                os.remove(user.profile_photo)  # Удаление старого файла
            except Exception as e:
                logging.error(f"Error removing old file: {e}")
        
        # Определяем новое имя файла с оригинальным расширением и добавляем timestamp
        timestamp = int(datetime.utcnow().timestamp())
        file_extension = file.filename.split(".")[-1]  # Например, "jpg" или "png"
        new_file_name = f"{user_id}_{timestamp}.{file_extension}"
        new_file_path = os.path.join(UPLOAD_DIR, new_file_name)
        
        # Сохраняем новый файл
        try:
            with open(new_file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
        except Exception as e:
            logging.error(f"Error saving file: {e}")
            return {"error": f"Could not save file: {str(e)}"}
        
        # Обновляем запись в базе с новым путем
        user.profile_photo = new_file_path
        await user.save()
        
        return {"message": "Profile photo updated successfully", "photo_url": new_file_path}

    async def get_profile_photo(self, user_id: str):
        user = await User.get(user_id)
        if not user or not user.profile_photo:
            raise HTTPException(status_code=404, detail="Photo not found")
        
        file_path = user.profile_photo
        
        logging.debug(f"File Path: {file_path}")
        print(file_path)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Profile photo file not found")
        
        return FileResponse(
            file_path, 
            media_type="image/*",
            headers={
                "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
                "Pragma": "no-cache",
                "Expires": "0",
            }
        )