import datetime
from enum import Enum
from typing import List, Optional
from beanie import Document
from pydantic import BaseModel, Field

from src.models.question import Question
from src.models.enums import QuizSubject, QuizType


DEFAULT_SUBJECTS = [
    {"subject": QuizSubject.HISTORY_KZ, "question_count": 20},
    {"subject": QuizSubject.MAT_GRAMOTNOST, "question_count": 20},
    {"subject": QuizSubject.READING_LITERACY, "question_count": 20},
]

class QuizStructure(BaseModel):
    subject: QuizSubject
    question_count: int

class Quiz(Document):
    variant: str 
    year: str
    title: str
    structure: List[QuizStructure] = [QuizStructure(**sub) for sub in DEFAULT_SUBJECTS]

    class Settings:
        collection = "quizzes"
    
    async def add_subjects(self, new_subjects: List[QuizStructure]):
        """Добавляет новые предметы к обязательным, если их еще нет"""
        existing_subjects = {s.subject for s in self.structure}  
        
        for subject in new_subjects:
            if subject.subject not in existing_subjects:
                self.structure.append(subject)
        
        await self.save()