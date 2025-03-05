from pydantic import BaseModel
from typing import List
from src.models.quiz import QuizStructure
from src.models.enums import QuestionType, QuizSubject
from src.models.enums import QuizSubject


class QuestionOptionDTO(BaseModel):
    label: str  # A, B, C, D, E
    option_text: str
    is_correct: bool = False

class QuestionDTO(BaseModel):
    type: QuestionType
    subject: QuizSubject
    question_text: str
    options: List[QuestionOptionDTO]

class QuizCreateDTO(BaseModel):
    title: str
    year: str
    variant: str
    subjects: List[QuizStructure]

class QuizAttemptDTO(BaseModel):
    user_id: str
    quiz_id: str

