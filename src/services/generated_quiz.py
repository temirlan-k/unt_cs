from datetime import datetime
import json
from typing import List
from beanie import PydanticObjectId
from src.schemas.req.generated_quiz import UserAnswerRequest
from src.models.generated_quiz import GeneratedQuiz, GeneratedQuestion, QuestionOption, UserAnswer, UserGeneratedQuizAttempt
from src.helpers.llm import LLMClient
from fastapi import HTTPException



class QuizGeneratorService:

    async def generate_quiz(self, user_prompt: str, user_id:PydanticObjectId) -> GeneratedQuiz:
        llm_client = LLMClient()
            
        response = await llm_client.generate_response(user_prompt)

        quiz_data = json.loads(response)

        questions = [
            GeneratedQuestion(
                id=PydanticObjectId(),
                type=question_data["type"],
                question_text=question_data["question_text"],
                options=[QuestionOption(**option) for option in question_data["options"]]
            )
            for question_data in quiz_data["questions"]
        ]
        generated_quiz = GeneratedQuiz(
            user_id=user_id, 
            title=quiz_data["title"],
            subject=quiz_data["subject"],
            questions=questions
        )
        await generated_quiz.insert()

        return generated_quiz

    async def get_user_attempts(self, user_id: PydanticObjectId):
        """Получает все попытки прохождения тестов пользователем"""
        return await UserGeneratedQuizAttempt.find(UserGeneratedQuizAttempt.user_id == user_id).to_list()

    async def get_all_quizzes(self):
        return await GeneratedQuiz.find_all().to_list()
    
    async def get_quizzes_by_user(self, user_id: PydanticObjectId):
        return await GeneratedQuiz.find(GeneratedQuiz.user_id == user_id).to_list()
    
    async def start_quiz_attempt(self, user_id: PydanticObjectId, quiz_id: PydanticObjectId):
        attempt = UserGeneratedQuizAttempt(
            user_id=user_id,
            quiz_id=quiz_id,
            started_at=datetime.utcnow()
        )
        await attempt.insert()
        return attempt
    

    async def submit_quiz_attempt(self, attempt_id: PydanticObjectId, answers: List[UserAnswer]):
        attempt = await UserGeneratedQuizAttempt.get(attempt_id)
        if not attempt:
            raise HTTPException(status_code=404, detail='Attempt not found')


        quiz = await GeneratedQuiz.get(attempt.quiz_id)
        if not quiz:
            raise HTTPException(status_code=404, detail='Quiz not found')

        total_score = 0

        for answer in answers:
            question = next((q for q in quiz.questions if q.id == answer.question_id), None)
            if not question:
                continue

            correct_options = [opt.label for opt in question.options if opt.is_correct]
            selected_correct = len(set(answer.selected_options) & set(correct_options))
            total_correct = len(correct_options)

            if question.type == "single_choice":
                # Один правильный ответ, 1 балл за правильный выбор
                answer.score = 1 if selected_correct == 1 else 0

            elif question.type == "multiple_choice":
                # Если выбрал все правильные — 2 балла, если не все — 1 балл, если ничего или ошибся — 0 баллов
                if selected_correct == total_correct:
                    answer.score = 2
                elif selected_correct > 0:
                    answer.score = 1
                else:
                    answer.score = 0

            total_score += answer.score

        attempt.answers = answers
        attempt.score = total_score
        attempt.finished_at = datetime.utcnow()

        await attempt.save()
        return attempt
    
    
    async def answer_question(
        self, 
        attempt_id: PydanticObjectId, 
        answer: UserAnswerRequest
    ):
        """Добавляет ответ на вопрос в текущую попытку"""
        attempt = await UserGeneratedQuizAttempt.get(attempt_id)
        if not attempt:
            raise HTTPException(status_code=404, detail="Attempt not found")

        if attempt.finished_at:
            raise HTTPException(status_code=400, detail="Attempt already finished")

        quiz = await GeneratedQuiz.get(attempt.quiz_id)
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        question = next((q for q in quiz.questions if q.id == answer.question_id), None)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        # Проверка, был ли уже дан ответ на этот вопрос в текущей попытке
        if any(ans.question_id == answer.question_id for ans in attempt.answers):
            raise HTTPException(status_code=400, detail="Question already answered in this attempt")

        # Подсчет баллов
        correct_options = {opt.label for opt in question.options if opt.is_correct}
        selected_options = set(answer.selected_options)

        selected_correct = len(selected_options & correct_options)
        total_correct = len(correct_options)

        score = 0
        if question.type == "single_choice":
            score = 1 if selected_correct == 1 else 0
        elif question.type == "multiple_choice":
            if selected_options == correct_options:  # Полностью правильный ответ
                score = 2
            elif selected_correct > 0 and selected_options.issubset(correct_options):  # Частично правильный без ошибок
                score = 1
            else:  # Если есть хотя бы одна ошибка
                score = 0

        user_answer = UserAnswer(
            question_id=answer.question_id,
            selected_options=answer.selected_options,
            score=score
        )

        if attempt.score is None:
            attempt.score = 0
        attempt.answers.append(user_answer)
        attempt.score += score

        await attempt.save()
        return {"message": "Answer submitted", "score": score}
