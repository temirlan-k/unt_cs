from beanie import PydanticObjectId
from fastapi import APIRouter, Depends
from typing import List
from src.services.generated_quiz import QuizGeneratorService
from src.schemas.req.generated_quiz import QuizGenerationRequest
from src.models.user_answer import AnswerCreate, UserAnswer
from src.core.auth_middleware import get_current_user
from src.schemas.req.quiz import QuizCreateDTO, QuizAttemptDTO, QuestionDTO
from src.services.quiz import QuizService
from src.models.quiz import Quiz
from src.models.quiz_session import UserQuizAttempt
from src.models.enums import QuizSubject

generated_quiz_router = APIRouter()


@generated_quiz_router.post('/generated_quiz')
async def generate_quiz(
    user_prompt:QuizGenerationRequest,
    quiz_generator_service: QuizGeneratorService = Depends(QuizGeneratorService),
    token: dict = Depends(get_current_user),
):
    return await quiz_generator_service.generate_quiz(user_prompt.user_prompt, PydanticObjectId(token.get('sub')))

@generated_quiz_router.get("/generated_quizzes",)
async def get_all_quizzes(service: QuizGeneratorService = Depends(QuizGeneratorService)):
    return await service.get_all_quizzes()


@generated_quiz_router.get("/generated_quizzes/me",)
async def get_user_quizzes(
    token: dict = Depends(get_current_user),
    service: QuizGeneratorService = Depends(QuizGeneratorService)
):
    user_id = PydanticObjectId(token.get("sub"))
    return await service.get_quizzes_by_user(user_id)


@generated_quiz_router.post("/generated_quizzes/{quiz_id}/start", )
async def start_quiz_attempt(
    quiz_id: PydanticObjectId,
    token: dict = Depends(get_current_user),
    service: QuizGeneratorService = Depends(QuizGeneratorService)
):
    user_id = PydanticObjectId(token.get("sub"))
    return await service.start_quiz_attempt( quiz_id,user_id)

@generated_quiz_router.post("/generated_quizzes/{attempt_id}/submit", )
async def submit_quiz_attempt(
    attempt_id: PydanticObjectId,
    answers: List[UserAnswer],
    service: QuizGeneratorService = Depends(QuizGeneratorService)
):
    return await service.submit_quiz_attempt(attempt_id, answers)

@generated_quiz_router.get("/generated_quizzes/attempts/me",)
async def get_user_attempts(
    token: dict = Depends(get_current_user),
    service: QuizGeneratorService = Depends(QuizGeneratorService)
):
    user_id = PydanticObjectId(token.get("sub"))
    return await service.get_user_attempts(user_id)
