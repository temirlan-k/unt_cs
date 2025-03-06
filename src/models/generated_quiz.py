from enum import Enum
from typing import List
from beanie import Document, PydanticObjectId
from pydantic import BaseModel

# Определяем возможные типы вопросов
class QuestionType(str, Enum):
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"

# Опции для вопросов
class QuestionOption(BaseModel):
    label: str  # A, B, C, D (single_choice) / A-H (multiple_choice)
    option_text: str
    is_correct: bool = False

# Модель вопроса
class GeneratedQuestion(BaseModel):
    type: QuestionType
    question_text: str
    options: List[QuestionOption]

# Основная модель теста
class GeneratedQuiz(Document):
    title: str  # AI-сгенерированное название теста
    subject: str  # Основная тема теста
    questions: List[GeneratedQuestion]  # Список вопросов

    class Settings:
        collection = "generated_quizzes"
