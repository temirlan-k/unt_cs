from beanie import Document, PydanticObjectId
from pydantic import BaseModel

class AnswerCreate(BaseModel):
    """Модель для отправки ответа на вопрос"""
    question_id: PydanticObjectId
    option_label: str  # A, B, C, D, E, F, G


class UserAnswer(Document):
    """Ответ пользователя на вопрос в квизе"""
    attempt_id: PydanticObjectId  # ID попытки
    question_id: PydanticObjectId  # ID вопроса
    selected_option: str  # Выбранный вариант (A, B, C и т.д.)
    is_correct: bool  # Был ли ответ правильным

    class Settings:
        collection = "user_answers"
