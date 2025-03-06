from datetime import datetime
from beanie import Document
from pydantic import BaseModel
from typing import List
from beanie import PydanticObjectId


class MistakeBank(Document):
    user_id: PydanticObjectId
    question_id: PydanticObjectId
    quiz_id: PydanticObjectId
    question_text: str
    options: List[dict]
    added_at: datetime = datetime.utcnow()

    class Settings:
        collection = "mistake_bank"
