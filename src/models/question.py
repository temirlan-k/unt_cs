import datetime
from enum import Enum
from typing import List, Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from src.models.enums import *

class QuestionOption(BaseModel):
    label: str  # A, B, C, D, E, F, G
    option_text: str
    is_correct: bool = False


class Question(Document):   
    quiz_id: PydanticObjectId 
    type: QuestionType
    subject: QuizSubject
    question_text: str
    options: List[QuestionOption]

    class Settings:
        collection = "questions"


