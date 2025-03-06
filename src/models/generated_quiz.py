from enum import Enum
from typing import List
from beanie import Document, PydanticObjectId
from pydantic import BaseModel

class QuestionType(str, Enum):
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"

class QuestionOption(BaseModel):
    label: str  # A, B, C, D (single_choice) / A-H (multiple_choice)
    option_text: str
    is_correct: bool = False

class GeneratedQuestion(BaseModel):
    type: QuestionType
    question_text: str
    options: List[QuestionOption]

class GeneratedQuiz(Document):
    user_id:PydanticObjectId
    title: str  
    subject: str 
    questions: List[GeneratedQuestion] 

    class Settings:
        collection = "generated_quizzes"
