from beanie import PydanticObjectId
from fastapi import HTTPException
from datetime import datetime
from src.models.generated_quiz import GeneratedQuiz
from src.schemas.req.generated_quiz import UserAnswerRequest
from src.schemas.res.question import OptionResponse, QuestionResponse
from src.models.user_answer import AnswerCreate, UserAnswer
from src.models.user import User
from src.models.quiz import Quiz, QuizStructure
from src.models.question import Question
from src.models.quiz_session import UserQuizAttempt
from src.schemas.req.quiz import QuizCreateDTO, QuestionDTO
from src.models.enums import QuizSubject, QuestionType
from src.models.mistake_bank import MistakeBankQuiz
from fastapi.encoders import jsonable_encoder


class MistakeBankQuizService:

    async def start_mistake_bank_quiz(self, user_id: PydanticObjectId):
        """Запускает MistakeBank квиз для пользователя (возвращает все вопросы с ошибками)."""
        mistakes = await MistakeBankQuiz.find(MistakeBankQuiz.user_id == user_id).to_list()
        if not mistakes:
            raise HTTPException(status_code=404, detail="No mistakes found")

        # Формируем список вопросов
        questions = [
            {
                "question_id": str(mistake.question_id),
                "question_text": mistake.question_text,
                "options": mistake.options
            }
            for mistake in mistakes
        ]
        return {"questions": questions}

    async def answer_question_for_mistake_bank_quiz(
        self, 
        user_id: PydanticObjectId, 
        answer: UserAnswerRequest
    ):
        """Ответ на вопрос MistakeBank квиза (без начисления баллов), если ответ правильный, удаляется из MistakeBank."""
        # Находим вопрос в MistakeBank для этого пользователя
        mistake = await MistakeBankQuiz.find_one(
            MistakeBankQuiz.user_id == user_id, MistakeBankQuiz.question_id == answer.question_id
        )
        if not mistake:
            raise HTTPException(status_code=404, detail="Mistake question not found")

        question = mistake
        if not question:
            question = mistake

        if not question:
            raise HTTPException(status_code=404, detail="Quiz not found")

        # Получаем правильные ответы из вопроса
        correct_options = {opt['label'] for opt in question.options if opt['is_correct']}
        selected_options = set(answer.selected_options)

        # Проверяем правильность ответа
        selected_correct = len(selected_options & correct_options)

        # Если ответ правильный, удаляем вопрос из MistakeBank
        if selected_correct == len(correct_options):
            await mistake.delete()

        return {"message": "Answer submitted", "correct": selected_correct == len(correct_options)}
