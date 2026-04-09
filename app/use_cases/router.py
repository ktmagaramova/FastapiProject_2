from fastapi import APIRouter
from app.use_cases import user, post, categorie, location, comment

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user.router)
api_router.include_router(post.router)
api_router.include_router(categorie.router)
api_router.include_router(location.router)
api_router.include_router(comment.router)