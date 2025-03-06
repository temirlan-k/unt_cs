from datetime import datetime
from beanie import Document, PydanticObjectId


class UserQuizAttempt(Document):
    quiz_id:PydanticObjectId
    user_id:PydanticObjectId
    score: float = 0
    started_at: datetime = datetime.now()
    ended_at: datetime = None
    is_completed: bool = False

    class Settings:
        collection = "user_quiz_attempts"