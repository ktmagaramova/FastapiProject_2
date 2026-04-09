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

router = APIRouter(prefix="/comment", tags=["Comment"])
#комменты

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CommentRead)
async def create_comment(c: CommentCreate) -> CommentRead:
    with database.session() as db:
        db_comment = Comment(
            text=c.text,
            created_at=datetime.utcnow(),
            is_published=True,
            author_id=c.author_id,
            post_id=c.post_id
        )
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return CommentRead.model_validate(db_comment)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[CommentRead])
async def get_comments(skip: int = 0, limit: int = 100) -> list[CommentRead]:
    with database.session() as db:
        comments = db.query(Comment).offset(skip).limit(limit).all()
        return [CommentRead.model_validate(c) for c in comments]


@router.get("/{post_id}/comments", status_code=status.HTTP_200_OK, response_model=list[CommentRead])
async def get_post_comments(post_id: int, skip: int = 0, limit: int = 100) -> list[CommentRead]:
    with database.session() as db:
        comments = db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()
        return [CommentRead.model_validate(c) for c in comments]


@router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment(comment_id: int) -> dict:
    with database.session() as db:
        db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
        db.delete(db_comment)
        db.commit()
        return {"detail": "Комментарий удалён"}