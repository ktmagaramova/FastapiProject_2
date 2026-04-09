from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from app.models import Post, User, Category, Location, Comment
from app.schemas import (
    PostCreate, PostRead, PostUpdate,
    UserCreate, UserRead,
    CategoryCreate, CategoryRead,
    LocationCreate, LocationRead,
    CommentCreate, CommentRead
)
from app.database import database
from datetime import datetime

router = APIRouter()
router = APIRouter(prefix="/user", tags=["Users"])
#пользователь
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserRead)
def create_user(u: UserCreate) -> UserRead:
    with database.session() as db:
        db_user = User(
            password=u.password,
            username=u.username,
            first_name=u.first_name or "",
            last_name=u.last_name or "",
            email=u.email or "",
            is_active=True,
            is_staff=False,
            is_superuser=False,
            last_login=None,
            date_joined=datetime.utcnow()
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return UserRead.model_validate(db_user)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[UserRead])
async def get_users(skip: int = 0, limit: int = 100) -> list[UserRead]:
    with database.session() as db:
        users = db.query(User).offset(skip).limit(limit).all()
        return [UserRead.model_validate(u) for u in users]


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserRead)
async def get_user(user_id: int) -> UserRead:
    with database.session() as db:
        user = db.query(User).filter(User.id == user_id).first()
        return UserRead.model_validate(user)


@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserRead)
async def update_user(user_id: int, user_data: UserCreate) -> UserRead:
    with database.session() as db:
        db_user = db.query(User).filter(User.id == user_id).first()
        db_user.username = user_data.username
        db_user.password = user_data.password
        db_user.first_name = user_data.first_name or ""
        db_user.last_name = user_data.last_name or ""
        db_user.email = user_data.email or ""
        db.commit()
        db.refresh(db_user)
        return UserRead.model_validate(db_user)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int) -> dict:
    with database.session() as db:
        db_user = db.query(User).filter(User.id == user_id).first()
        db.delete(db_user)
        db.commit()
        return {"detail": "Пользователь удалён"}

