from fastapi import APIRouter, Depends
from typing import List
from src.schemas.req.quiz import QuizCreateDTO, QuizAttemptDTO, QuestionDTO
from src.services.quiz import QuizService
from src.models.quiz import Quiz
from src.models.quiz_session import UserQuizAttempt

quiz_router = APIRouter()

@quiz_router.post("/", response_model=Quiz)
async def create_quiz(quiz_data: QuizCreateDTO, quiz_service: QuizService = Depends(QuizService)):
    """Создать новый квиз"""
    return await quiz_service.create_quiz(quiz_data)

@quiz_router.post("/{quiz_id}/questions", response_model=Quiz)
async def add_question(quiz_id: str, question_data: QuestionDTO, quiz_service: QuizService = Depends(QuizService)):
    """Добавить вопрос в квиз"""
    return await quiz_service.add_question(quiz_id, question_data)

@quiz_router.get("/", response_model=List[Quiz])
async def get_all_quizzes(quiz_service: QuizService = Depends(QuizService)):
    """Получить все квизы"""
    return await quiz_service.get_all_quizzes()

@quiz_router.post("/{quiz_id}/start", response_model=UserQuizAttempt)
async def start_quiz_attempt(quiz_id: str, user_id: str, quiz_service: QuizService = Depends(QuizService)):
    """Начать попытку квиза"""
    return await quiz_service.start_quiz_attempt(quiz_id, user_id)

@quiz_router.post("/attempts/{attempt_id}/submit", response_model=UserQuizAttempt)
async def submit_quiz_attempt(attempt_id: str, score: float, quiz_service: QuizService = Depends(QuizService)):
    """Завершить квиз"""
    return await quiz_service.submit_quiz_attempt(attempt_id, score)
