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
from src.models.mistake_bank import MistakeBankQuiz,MistakeQuizSession
from fastapi.encoders import jsonable_encoder


class MistakeBankQuizService:

    async def start_mistake_quiz_session(self, user_id: PydanticObjectId):
        """Создает новую сессию MistakeBank-квиза."""
        active_session = await MistakeQuizSession.find_one({"user_id": user_id, "status": "in_progress"})
        if active_session:
            raise HTTPException(status_code=400, detail="You already have an active mistake quiz session.")

        mistakes = await MistakeBankQuiz.find(MistakeBankQuiz.user_id == user_id).to_list()
        if not mistakes:
            raise HTTPException(status_code=404, detail="No mistakes found")

        session = MistakeQuizSession(user_id=user_id, mistakes=[])
        await session.insert()
        
        questions = [{
            "question_id": str(m.question_id),
            "question_text": m.question_text,
            "options": m.options
        } for m in mistakes]
        
        return {"session_id": str(session.id), "questions": questions}
    
    async def answer_mistake_question(self, user_id: PydanticObjectId, session_id: PydanticObjectId, answer: UserAnswerRequest):
        """Обрабатывает ответ пользователя в сессии MistakeBank-квиза."""
        session = await MistakeQuizSession.get(session_id)
        if not session or session.user_id != user_id:
            raise HTTPException(status_code=404, detail="Mistake quiz session not found")

        mistake = await MistakeBankQuiz.find_one(
            MistakeBankQuiz.user_id == user_id, MistakeBankQuiz.question_id == answer.question_id
        )
        if not mistake:
            raise HTTPException(status_code=404, detail="Mistake question not found")
        
        correct_options = {opt['label'] for opt in mistake.options if opt['is_correct']}
        selected_options = set(answer.selected_options)
        is_correct = selected_options == correct_options
        question = await MistakeBankQuiz.find_one(MistakeBankQuiz.question_id == answer.question_id)
        session.mistakes.append({
            "question_id": str(answer.question_id),
            "question_text":question.question_text,
            "options":question.options,
            "selected_options": answer.selected_options,
            "is_correct": is_correct
        })
        await session.save()
        
        if is_correct:
            await mistake.delete()
                
        return {"message": "Answer submitted", "correct": is_correct,"correct_options":correct_options,"selected_options":selected_options}
    
    async def complete_mistake_quiz_session(self, user_id: PydanticObjectId, session_id: PydanticObjectId):
        """Завершает MistakeBank-квиз сессию и удаляет правильно отвеченные вопросы."""
        session = await MistakeQuizSession.get(session_id)
        if not session or session.user_id != user_id:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session.status = "completed"
        session.completed_at = datetime.utcnow()
        await session.save()
        
        # Удаляем все вопросы из MistakeBankQuiz, на которые ответили правильно
        for mistake in session.mistakes:
            if mistake["is_correct"]:
                await MistakeBankQuiz.find_one(MistakeBankQuiz.user_id == user_id, MistakeBankQuiz.question_id == mistake["question_id"]).delete()
        
        return {"message": "Mistake quiz session completed", "session_results": session.mistakes}

    async def get_mistake_quiz_session_results(self, user_id, session_id, ):
        session = await MistakeQuizSession.get(session_id)
        if not session or session.user_id != (user_id):
            raise HTTPException(status_code=404, detail="Session not found")

        return {"session_id": str(session.id), "mistakes": session.mistakes}
    
    async def get_all_mistake_quiz_sessions(self, user_id):
        sessions = await MistakeQuizSession.find(MistakeQuizSession.user_id == user_id).to_list()
        return sessions
    
    async def get_all_questions_from_mistake(self,user_id:PydanticObjectId):
        mistakes = await MistakeBankQuiz.find(MistakeBankQuiz.user_id == user_id).to_list()
        if not mistakes:
            raise HTTPException(status_code=404, detail="No mistakes found")

        questions = [{
            "question_id": str(m.question_id),
            "question_text": m.question_text,
            "options": m.options
        } for m in mistakes]
        
        return questions
