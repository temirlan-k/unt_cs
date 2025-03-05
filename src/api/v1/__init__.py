from fastapi import APIRouter
from src.api.v1.auth import auth_router
from src.api.v1.profile import profile_router
from src.api.v1.quiz import quiz_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(profile_router,prefix="/profile",tags=["profile"])
api_router.include_router(quiz_router,prefix='/quiz',tags=['quiz'])