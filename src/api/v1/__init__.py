from fastapi import APIRouter
from src.api.v1.auth import auth_router
from src.api.v1.profile import profile_router
from src.api.v1.quiz import quiz_router
from src.api.v1.subject import quiz_enums
from src.api.v1.generated_quiz import generated_quiz_router
from src.api.v1.mistake_bank import mistake_bank_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(profile_router,prefix="/profile",tags=["profile"])
api_router.include_router(quiz_router,prefix='/quiz',tags=['quiz'])
api_router.include_router(quiz_enums,prefix='/quiz-enums',tags=['quiz-enums'])
api_router.include_router(generated_quiz_router,prefix='/generated-quiz',tags=['generated-quiz'])
api_router.include_router(mistake_bank_router,prefix='/mistake',tags=['mistakes'])