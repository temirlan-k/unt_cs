from pydantic import BaseModel


class QuizGenerationRequest(BaseModel):
    user_prompt: str