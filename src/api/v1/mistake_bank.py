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

@mistake_bank_router.get("/start_mistake_quiz_session/")
async def start_mistake_quiz_session(
    token: dict = Depends(get_current_user),
    mistake_bank_quiz_service: MistakeBankQuizService = Depends(MistakeBankQuizService)
):
    """
    Запускает новую сессию MistakeBank-квиза.
    """
    return await mistake_bank_quiz_service.start_mistake_quiz_session(PydanticObjectId(token.get('sub')))

@mistake_bank_router.post("/answer_mistake_question/")
async def answer_mistake_question(
    session_id: PydanticObjectId,
    answer: UserAnswerRequest,
    token: dict = Depends(get_current_user),
    mistake_bank_quiz_service: MistakeBankQuizService = Depends(MistakeBankQuizService)
):
    """
    Отвечает на вопрос в MistakeBank-квизе.
    """
    return await mistake_bank_quiz_service.answer_mistake_question(PydanticObjectId(token.get('sub')), session_id, answer)

@mistake_bank_router.post("/complete_mistake_quiz_session/")
async def complete_mistake_quiz_session(
    session_id: PydanticObjectId,
    token: dict = Depends(get_current_user),
    mistake_bank_quiz_service: MistakeBankQuizService = Depends(MistakeBankQuizService)
):
    """
    Завершает MistakeBank-квиз сессию и удаляет правильно отвеченные вопросы.
    """
    return await mistake_bank_quiz_service.complete_mistake_quiz_session(PydanticObjectId(token.get('sub')), session_id)

@mistake_bank_router.get("/mistake_quiz_session_results/{session_id}")
async def get_mistake_quiz_session_results(
    session_id: PydanticObjectId,
    token: dict = Depends(get_current_user),
    mistake_bank_quiz_service: MistakeBankQuizService = Depends(MistakeBankQuizService)
):
    """
    Получает результаты MistakeBank-квиз сессии без завершения.
    """
    return await mistake_bank_quiz_service.get_mistake_quiz_session_results(PydanticObjectId(token.get('sub')), session_id)


@mistake_bank_router.get("/all_mistake_quiz_sessions/")
async def get_all_mistake_quiz_sessions(
    token: dict = Depends(get_current_user),
    mistake_bank_quiz_service: MistakeBankQuizService = Depends()
):
    return await mistake_bank_quiz_service.get_all_mistake_quiz_sessions(PydanticObjectId(token.get('sub')))


#Ручка для получения всех вопросов из MistakeBank
@mistake_bank_router.get("/get_all_questions_from_mistake/", )
async def get_all_questions_from_mistake(       
    token: dict = Depends(get_current_user),
    mistake_bank_quiz_service: MistakeBankQuizService = Depends(MistakeBankQuizService)
):
    """
    Возвращает все вопросы, которые пользователь ошибся в прошлом.
    """
    return await mistake_bank_quiz_service.get_all_questions_from_mistake(PydanticObjectId(token.get('sub')))

