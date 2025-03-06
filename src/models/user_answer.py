from typing import List
from beanie import Document, PydanticObjectId
from pydantic import BaseModel


class AnswerCreate(BaseModel):
    """Модель для отправки ответа на вопрос (с поддержкой нескольких вариантов)"""
    question_id: PydanticObjectId
    option_labels: List[str]  # Список выбранных вариантов (["A", "C"])


class UserAnswer(Document):
    """Ответ пользователя на вопрос в квизе"""
    attempt_id: PydanticObjectId  # ID попытки
    question_id: PydanticObjectId  # ID вопроса
    selected_options: List[str]  # Выбранные варианты (["A", "C"])
    score: float

    class Settings:
        collection = "user_answers"