
from beanie import PydanticObjectId
from pydantic import BaseModel


class OptionResponse(BaseModel):
    label: str
    option_text: str  

class QuestionResponse(BaseModel):
    id: PydanticObjectId
    quiz_id: PydanticObjectId
    type: str
    subject: str
    question_text: str
    options: list[OptionResponse]