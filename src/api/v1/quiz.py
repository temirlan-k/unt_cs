from fastapi import APIRouter, Depends
from typing import List
from src.core.auth_middleware import get_current_user
from src.schemas.req.quiz import QuizCreateDTO, QuizAttemptDTO, QuestionDTO
from src.services.quiz import QuizService
from src.models.quiz import Quiz
from src.models.quiz_session import UserQuizAttempt

quiz_router = APIRouter()

@quiz_router.post("/", )
async def create_quiz(quiz_data: QuizCreateDTO, quiz_service: QuizService = Depends(QuizService)):
    """Создать новый квиз"""
    return await quiz_service.create_quiz(quiz_data)

@quiz_router.post("/{quiz_id}/questions", )
async def add_question(quiz_id: str, question_data: QuestionDTO, quiz_service: QuizService = Depends(QuizService)):
    """Добавить вопрос в квиз"""
    return await quiz_service.add_question(quiz_id, question_data)

@quiz_router.get("/", )
async def get_all_quizzes(quiz_service: QuizService = Depends(QuizService)):
    """Получить все квизы"""
    return await quiz_service.get_all_quizzes()

@quiz_router.post("/{quiz_id}/start", )
async def start_quiz_attempt(
    quiz_id: str, 
    quiz_service: QuizService = Depends(QuizService),
    token: dict = Depends(get_current_user),
):
    """Начать попытку квиза"""
    return await quiz_service.start_quiz_attempt(quiz_id, token.get('sub'))

@quiz_router.post("/attempts/{attempt_id}/submit", )
async def submit_quiz_attempt(
    attempt_id: str, 
    quiz_service: QuizService = Depends(QuizService),
    token: dict = Depends(get_current_user),
):
    """Завершить квиз"""
    return await quiz_service.submit_quiz_attempt(attempt_id, token.get('sub'))


