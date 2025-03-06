from typing import List
from beanie import PydanticObjectId
from pydantic import BaseModel


class QuizGenerationRequest(BaseModel):
    user_prompt: str

class UserAnswerRequest(BaseModel):
    question_id: PydanticObjectId
    selected_options: List[str]  # Выбранные варианты (например, ["A", "C"])