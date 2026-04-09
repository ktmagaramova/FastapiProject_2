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
router = APIRouter(prefix="/post", tags=["Post"])
#посты
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[PostRead])
async def get_posts(skip: int = 0, limit: int = 100) -> list[PostRead]:
    with database.session() as db:
        posts = db.query(Post).offset(skip).limit(limit).all()
        return [PostRead.model_validate(p) for p in posts[::-1]]


@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostRead)
async def get_post(post_id: int) -> PostRead:
    with database.session() as db:
        post = db.query(Post).filter(Post.id == post_id).first()
        return PostRead.model_validate(post)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostRead)
async def create_post(p: PostCreate) -> PostRead:
    with database.session() as db:
        db_post = Post(
            title=p.title,
            text=p.text,
            pub_date=p.pub_date,
            image=p.image or "",
            is_published=True,
            created_at=datetime.utcnow(),
            author_id=p.author_id,
            category_id=p.category_id,
            location_id=p.location_id
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return PostRead.model_validate(db_post)


@router.put("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostRead)
async def update_post(post_id: int, updated_post_data: PostUpdate) -> PostRead:
    with database.session() as db:
        db_post = db.query(Post).filter(Post.id == post_id).first()
        if updated_post_data.title is not None:
            db_post.title = updated_post_data.title
        if updated_post_data.text is not None:
            db_post.text = updated_post_data.text
        if updated_post_data.pub_date is not None:
            db_post.pub_date = updated_post_data.pub_date
        if updated_post_data.image is not None:
            db_post.image = updated_post_data.image
        if updated_post_data.category_id is not None:
            db_post.category_id = updated_post_data.category_id
        if updated_post_data.location_id is not None:
            db_post.location_id = updated_post_data.location_id
        db.commit()
        db.refresh(db_post)
        return PostRead.model_validate(db_post)


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int) -> dict:
    with database.session() as db:
        db_post = db.query(Post).filter(Post.id == post_id).first()
        db.delete(db_post)
        db.commit()
        return {"detail": "Пост удалён"}

