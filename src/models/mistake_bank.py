from datetime import datetime
from beanie import Document
from pydantic import BaseModel
from typing import List, Optional
from beanie import PydanticObjectId


class MistakeBankQuiz(Document):
    user_id: PydanticObjectId
    question_id: PydanticObjectId
    quiz_id: PydanticObjectId
    question_text: str
    options: List[dict]
    added_at: datetime = datetime.utcnow()

    class Settings:
        collection = "mistake_bank"



class MistakeQuizSession(Document):
    user_id: PydanticObjectId
    started_at: datetime = datetime.utcnow()
    completed_at: Optional[datetime] = None
    mistakes: List[dict] = []  # [{'question_id': ..., 'selected_options': [...], 'is_correct': ...}]
    status: str = "in_progress"  # in_progress, completed

    class Settings:
        collection = "mistake_quiz_sessions"

