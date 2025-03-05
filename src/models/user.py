import datetime
from enum import Enum
from typing import Optional

from beanie import Document

class UserRoleEnum(str,Enum):
    STUDENT = "student"
    ADMIN = 'admin'

class User(Document):
    first_name: str
    last_name: str
    role:UserRoleEnum = UserRoleEnum.STUDENT
    email: str
    password: str
    total_score: int = 0

    class Settings:
        collection = "users"
