import os
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from src.models.mistake_bank import MistakeBankQuiz, MistakeQuizSession
from src.models.generated_quiz import GeneratedQuiz, UserGeneratedQuizAttempt
from src.models.user import User
from src.models.question import *
from src.models.quiz import *
from src.models.quiz_session import UserQuizAttempt
from src.models.user_answer import UserAnswer

client = None
db = None


async def init_db():
    global client, db
    client = AsyncIOMotorClient(os.getenv("DB_URL"))
    db = client.unt_cs
    await init_beanie(
        database=db,
        document_models=[
            User,
            Question,
            Quiz,
            UserAnswer,
            UserQuizAttempt,
            GeneratedQuiz,
            UserGeneratedQuizAttempt,
            MistakeBankQuiz,
            MistakeQuizSession,
        ],
    )
