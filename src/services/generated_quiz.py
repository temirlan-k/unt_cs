import json
from beanie import PydanticObjectId
from src.models.generated_quiz import GeneratedQuiz, GeneratedQuestion, QuestionOption
from src.helpers.llm import LLMClient



class QuizGeneratorService:

    async def generate_quiz(self, user_prompt: str, user_id:PydanticObjectId) -> GeneratedQuiz:
        llm_client = LLMClient()
            
        response = await llm_client.generate_response(user_prompt)

        quiz_data = json.loads(response)

        questions = [
            GeneratedQuestion(
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
