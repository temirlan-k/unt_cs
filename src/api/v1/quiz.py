from beanie import PydanticObjectId
from fastapi import APIRouter, Depends
from typing import List
from src.models.user_answer import AnswerCreate, UserAnswer
from src.core.auth_middleware import get_current_user
from src.schemas.req.quiz import QuizCreateDTO, QuizAttemptDTO, QuestionDTO
from src.services.quiz import QuizService
from src.models.quiz import Quiz
from src.models.quiz_session import UserQuizAttempt
from src.models.enums import QuizSubject

quiz_router = APIRouter()

@quiz_router.post("/", )
async def create_quiz(quiz_data: QuizCreateDTO, quiz_service: QuizService = Depends(QuizService)):
    """Создать новый квиз"""
    return await quiz_service.create_quiz(quiz_data)

@quiz_router.post("/{quiz_id}/questions", )
async def add_question(quiz_id: PydanticObjectId, question_data: QuestionDTO, quiz_service: QuizService = Depends(QuizService)):
    """Добавить вопрос в квиз"""
    return await quiz_service.add_question(quiz_id, question_data)

@quiz_router.get("/", )
async def get_all_quizzes(quiz_service: QuizService = Depends(QuizService)):
    """Получить все квизы"""
    return await quiz_service.get_all_quizzes()

@quiz_router.post("/{quiz_id}/start", )
async def start_quiz_attempt(
    quiz_id: PydanticObjectId, 
    quiz_service: QuizService = Depends(QuizService),
    token: dict = Depends(get_current_user),
):
    """Начать попытку квиза"""
    return await quiz_service.start_quiz_attempt(quiz_id, PydanticObjectId(token.get('sub')))

@quiz_router.post("/attempts/{attempt_id}/finish", )
async def finish_quiz_attempt(
    attempt_id: PydanticObjectId, 
    quiz_service: QuizService = Depends(QuizService),
    token: dict = Depends(get_current_user),
):
    """Завершить квиз"""
    return await quiz_service.submit_quiz_attempt(attempt_id, PydanticObjectId(token.get('sub')))


@quiz_router.post("/attempts/{attempt_id}/answer")
async def submit_answer(
    attempt_id: PydanticObjectId, 
    answer_data: AnswerCreate,
    quiz_service: QuizService = Depends(QuizService),
    token: dict = Depends(get_current_user),
):
    """Ответить на вопрос в квизе"""
    return await quiz_service.submit_answer(attempt_id, answer_data, PydanticObjectId(token.get('sub')))

@quiz_router.get("/{quiz_id}/questions", )
async def get_quiz_questions(
    quiz_id: PydanticObjectId,
    quiz_service: QuizService = Depends(QuizService),
    token: dict = Depends(get_current_user),
):
    """Получить список вопросов для квиза"""
    return await quiz_service.get_quiz_questions(quiz_id)



@quiz_router.get("/attempts/me", )
async def get_user_quiz_attempts(
    quiz_service: QuizService = Depends(QuizService),
    token: dict = Depends(get_current_user),
):
    """Получить список историю попыток куизов"""
    return await quiz_service.get_user_quiz_attempts(PydanticObjectId(token.get('sub')))




@quiz_router.get("/{attempt_id}/attempt_details", )
async def get_detailed_answers(
    attempt_id: PydanticObjectId, 
    quiz_service: QuizService = Depends(QuizService),
    token: dict = Depends(get_current_user),
):
    """Получить детальные данные по попытке юзера"""
    return await quiz_service.get_attempt_details(attempt_id,PydanticObjectId(token.get('sub')))