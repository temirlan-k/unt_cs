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