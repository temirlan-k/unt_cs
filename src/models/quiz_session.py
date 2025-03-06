from datetime import datetime
from typing import Optional
from beanie import Document, PydanticObjectId


class UserQuizAttempt(Document):
    quiz_id:PydanticObjectId
    user_id:PydanticObjectId
    score: float 
    started_at: datetime = datetime.now()
    ended_at: Optional[datetime] = None
    is_completed: bool = False

    class Settings:
        collection = "user_quiz_attempts"