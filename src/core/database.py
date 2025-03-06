import os

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from src.models.user import User
from src.models.question import *
from src.models.quiz import *
from src.models.quiz_session import UserQuizAttempt
from src.models.user_answer import UserAnswer

client = None
db = None


async def init_db():
    global client, db
    client = AsyncIOMotorClient("mongodb://mongodb:27017/unt_cs")
    db = client.unt_cs
    await init_beanie(
        database=db,
        document_models=[
            User,
            Question,
            Quiz,
            UserAnswer,
            UserQuizAttempt
        ],
    )
