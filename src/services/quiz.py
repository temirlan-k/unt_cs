from beanie import PydanticObjectId
from fastapi import HTTPException
from src.models.user_answer import AnswerCreate, UserAnswer
from src.models.user import User
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
        await quiz.add_subjects(new_subjects)  
        return quiz

    async def add_question(self, quiz_id: PydanticObjectId, question_data: QuestionDTO):
        """Добавление вопроса в квиз"""
        quiz = await Quiz.get(quiz_id)
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        question = Question(quiz_id=quiz_id, **question_data.dict())
        await question.insert()
        return question

    async def get_all_quizzes(self):
        """Получение всех квизов"""
        return await Quiz.find_all().to_list()

    async def start_quiz_attempt(self, quiz_id: PydanticObjectId, user_id: PydanticObjectId):
        """Начало попытки квиза"""
        attempt = UserQuizAttempt(user_id=user_id, quiz_id=quiz_id,score=0)
        await attempt.insert()
        return attempt

    async def submit_quiz_attempt(self, attempt_id: PydanticObjectId,user_id:PydanticObjectId):
        """Завершение квиза с автоматическим расчетом балла"""
        attempt = await UserQuizAttempt.get(attempt_id)
        user = await User.get(user_id)
        if not attempt:
            raise HTTPException(status_code=404, detail="Quiz Attempt not found")

        questions = await Question.find({"quiz_id": attempt.quiz_id}).to_list()

        if not questions:
            raise HTTPException(status_code=400, detail="Questions not found")

        correct_answers = sum(
            1 for question in questions if any(option.is_correct for option in question.options)
        )
        total_questions = len(questions)

        score = round((correct_answers / total_questions) * 100, 2)

        attempt.score = score
        attempt.ended_at = datetime.utcnow()
        attempt.is_completed = True
        user.total_score += score
        await attempt.save()
        await user.save()

        return {
            "attempt_id": str(attempt.id),
            "quiz_id": str(attempt.quiz_id),
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "score": score
        }
    
    async def submit_answer(self, attempt_id: PydanticObjectId, answer_data: AnswerCreate, user_id: PydanticObjectId) -> UserAnswer:
        """Сохраняет ответ пользователя на вопрос и проверяет правильность"""
        attempt = await UserQuizAttempt.get(attempt_id)
        if not attempt:
            raise HTTPException(status_code=404,detail='Quiz attempt not found')
        if str(attempt.user_id) != user_id:
            raise HTTPException(status_code=403,detail="You cant rewrite someones quiz attempt")
        question = await Question.get(answer_data.question_id)
        if not question:
            raise HTTPException(status_code=404,detail='Question not found')

        # Проверяем, правильный ли ответ
        correct_option = next((opt for opt in question.options if opt.is_correct), None)
        is_correct = correct_option.label == answer_data.option_label if correct_option else False

        user_answer = UserAnswer(
            attempt_id=attempt_id,
            question_id=answer_data.question_id,
            selected_option=answer_data.option_label,
            is_correct=is_correct,
        )
        await user_answer.insert()

        return user_answer
    
    async def get_quiz_questions(self, quiz_id: PydanticObjectId):
        """Получить список вопросов для квиза"""
        questions = await Question.find(Question.quiz_id == quiz_id).to_list()
        return questions