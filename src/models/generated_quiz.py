from datetime import datetime
from enum import Enum
from typing import List, Optional
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
    id: PydanticObjectId = PydanticObjectId()
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

class UserAnswer(BaseModel):
    question_id: PydanticObjectId
    selected_options: List[str]
    score: int = 0

class UserGeneratedQuizAttempt(Document):
    user_id: PydanticObjectId
    quiz_id: PydanticObjectId
    answers: List[UserAnswer] = []
    score: Optional[int] = 0
    started_at: datetime
    finished_at: Optional[datetime] = None

    class Settings:
        collection = "user_generated_quiz_attempts"