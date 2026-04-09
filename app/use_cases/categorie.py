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
router = APIRouter(prefix="/categorie", tags=["Categorie"])
# категории
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CategoryRead)
def create_category(c: CategoryCreate) -> CategoryRead:
    with database.session() as db:
        db_category = Category(
            title=c.title,
            description=c.description or "",
            slug=c.slug or "",
            is_published=True,
            created_at=datetime.utcnow()
        )
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return CategoryRead.model_validate(db_category)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[CategoryRead])
async def get_categories(skip: int = 0, limit: int = 100) -> list[CategoryRead]:
    with database.session() as db:
        categories = db.query(Category).offset(skip).limit(limit).all()
        return [CategoryRead.model_validate(c) for c in categories]


@router.get("/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryRead)
async def get_category(category_id: int) -> CategoryRead:
    with database.session() as db:
        category = db.query(Category).filter(Category.id == category_id).first()
        return CategoryRead.model_validate(category)


@router.put("/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryRead)
async def update_category(category_id: int, category_data: CategoryCreate) -> CategoryRead:
    with database.session() as db:
        db_category = db.query(Category).filter(Category.id == category_id).first()
        db_category.title = category_data.title
        db_category.description = category_data.description or ""
        db_category.slug = category_data.slug or ""
        db.commit()
        db.refresh(db_category)
        return CategoryRead.model_validate(db_category)


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: int) -> dict:
    with database.session() as db:
        db_category = db.query(Category).filter(Category.id == category_id).first()
        db.delete(db_category)
        db.commit()
        return {"detail": "Категория удалена"}

