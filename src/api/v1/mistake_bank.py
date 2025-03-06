from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.core.auth_middleware import get_current_user
from src.models.generated_quiz import GeneratedQuiz
from src.models.mistake_bank import MistakeBankQuiz
from src.schemas.req.generated_quiz import UserAnswerRequest
from src.schemas.res.question import OptionResponse, QuestionResponse
from typing import List
from src.services.mistake_bank import MistakeBankQuizService

mistake_bank_router = APIRouter()


# Ручка для запуска MistakeBank квиза для пользователя
@mistake_bank_router.get("/start_mistake_bank_quiz/", )
async def start_mistake_bank_quiz( 
    token: dict = Depends(get_current_user),
    mistake_bank_quiz_service: MistakeBankQuizService = Depends(MistakeBankQuizService)
):
    """
    Запускает MistakeBank квиз для пользователя (возвращает все вопросы с ошибками).
    """
    return await mistake_bank_quiz_service.start_mistake_bank_quiz(PydanticObjectId(token.get('sub')))

# Ручка для ответа на вопрос MistakeBank квиза
@mistake_bank_router.post("/answer_question_for_mistake_bank_quiz/", response_model=dict)
async def answer_question_for_mistake_bank_quiz(
    answer: UserAnswerRequest,
    token: dict = Depends(get_current_user),
    mistake_bank_quiz_service: MistakeBankQuizService = Depends(MistakeBankQuizService)

):
    """
    Ответ на вопрос MistakeBank квиза (без начисления баллов),
    если ответ правильный, удаляется из MistakeBank.
    """
    return await mistake_bank_quiz_service.answer_question_for_mistake_bank_quiz(PydanticObjectId(token.get('sub')), answer)

# Ручка для получения всех вопросов из MistakeBank
@mistake_bank_router.get("/get_mistake_bank/", )
async def get_mistake_bank(    
    token: dict = Depends(get_current_user),
    mistake_bank_quiz_service: MistakeBankQuizService = Depends(MistakeBankQuizService)
):
    """
    Возвращает все вопросы, которые пользователь ошибся в прошлом.
    """
    return await mistake_bank_quiz_service.get_mistake_bank(PydanticObjectId(token.get('sub')))

# Ручка для проверки, пуст ли MistakeBank
@mistake_bank_router.get("/check_if_mistake_bank_is_empty/", response_model=dict)
async def check_if_mistake_bank_is_empty(    
    token: dict = Depends(get_current_user),
    mistake_bank_quiz_service: MistakeBankQuizService = Depends(MistakeBankQuizService)
):
    """
    Проверяет, все ли вопросы в MistakeBank были правильно отвечены.
    """
    return await mistake_bank_quiz_service.check_if_mistake_bank_is_empty(PydanticObjectId(token.get('sub')))
