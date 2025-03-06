import json
from beanie import PydanticObjectId
from src.models.generated_quiz import GeneratedQuiz, GeneratedQuestion, QuestionOption
from src.helpers.llm import LLMClient  # Клиент для работы с ИИ



class QuizGeneratorService:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def generate_quiz(self, user_prompt: str, user_id:PydanticObjectId) -> GeneratedQuiz:
        # Отправка запроса в ИИ
        response = await self.llm_client.generate_quiz(user_prompt)

        # Десериализация JSON-ответа
        quiz_data = json.loads(response)

        # Создание документа квиза
        generated_quiz = GeneratedQuiz(title=quiz_data["title"], subject=quiz_data["subject"])

        # Сохранение квиза в базу данных
        await generated_quiz.insert()

        # Обработка вопросов
        for question_data in quiz_data["questions"]:
            options = [
                QuestionOption(**option) for option in question_data["options"]
            ]

            generated_question = GeneratedQuestion(
                quiz_id=generated_quiz.id,
                type=question_data["type"],
                subject=quiz_data["subject"],
                question_text=question_data["question_text"],
                options=options,
            )

            await generated_question.insert()

        return generated_quiz
