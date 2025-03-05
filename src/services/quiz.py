from fastapi import HTTPException
from src.models.quiz import Quiz, QuizStructure
from src.models.question import Question
from src.models.quiz_session import UserQuizAttempt
from src.schemas.req.quiz import QuizCreateDTO
from src.schemas.req.quiz import QuestionDTO
from datetime import datetime

class QuizService:
    async def create_quiz(self, quiz_data: QuizCreateDTO):
        """Создание нового квиза"""
        quiz = Quiz(
            variant=quiz_data.variant,
            year=quiz_data.year,
            title=quiz_data.title,
        )        
        await quiz.insert()
        new_subjects = [
            QuizStructure(subject=sub.subject, question_count=sub.question_count)
            for sub in quiz_data.subjects  
        ]
        await quiz.add_subjects(new_subjects)  # Добавляем их к квизу
        return quiz

    async def add_question(self, quiz_id: str, question_data: QuestionDTO):
        """Добавление вопроса в квиз"""
        quiz = await Quiz.get(quiz_id)
        if not quiz:
            raise HTTPException(status_code=404, detail="Квиз не найден")

        question = Question(quiz_id=quiz_id, **question_data.dict())
        await question.insert()
        return question

    async def get_all_quizzes(self):
        """Получение всех квизов"""
        return await Quiz.find_all().to_list()

    async def start_quiz_attempt(self, quiz_id: str, user_id: str):
        """Начало попытки квиза"""
        attempt = UserQuizAttempt(user_id=user_id, quiz_id=quiz_id)
        await attempt.insert()
        return attempt

    async def submit_quiz_attempt(self, attempt_id: str, score: float):
        """Завершение квиза"""
        attempt = await UserQuizAttempt.get(attempt_id)
        if not attempt:
            raise HTTPException(status_code=404, detail="Попытка не найдена")

        attempt.score = score
        attempt.finished_at = datetime.utcnow()
        await attempt.save()
        return attempt
