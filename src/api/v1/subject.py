from fastapi import APIRouter, Depends
from typing import List
from src.schemas.req.quiz import QuizCreateDTO, QuizAttemptDTO, QuestionDTO
from src.services.quiz import QuizService
from src.models.quiz import Quiz
from src.models.quiz_session import UserQuizAttempt
from src.models.enums import *

quiz_enums = APIRouter()


@quiz_enums.get('/subjects')
async def subjects_list():
    return {"subjects": [subject.value for subject in QuizSubject]}


@quiz_enums.get('/quiz-types')
async def quiz_types_list():
    return {"quiz_types":[quiz_type.value for quiz_type in QuizType]}