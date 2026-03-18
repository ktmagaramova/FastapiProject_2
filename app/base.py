from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from app.models import Post, User, Category, Location
from app.schemas import (
    PostCreate, PostRead,
    UserCreate, UserRead,
    CategoryRead, CategoryCreate,
    LocationRead, LocationCreate
)
from app.database import database

router = APIRouter()


# Создание пользователя
@router.post("/user/", status_code=status.HTTP_201_CREATED, response_model=UserRead)
def create_user(u: UserCreate) -> UserRead:
    with database.session() as db:
        db_user = User(**u.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return UserRead.model_validate(db_user)


# Создание категории
@router.post("/categorie/", status_code=status.HTTP_201_CREATED, response_model=CategoryRead)
def create_category(c: CategoryCreate) -> CategoryRead:
    with database.session() as db:
        db_category = Category(**c.dict())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return CategoryRead.model_validate(db_category)


# Создание локации
@router.post("/location/", response_model=LocationRead, status_code=status.HTTP_201_CREATED)
def create_location(l: LocationCreate) -> LocationRead:
    with database.session() as db:
        db_location = Location(**l.dict())
        db.add(db_location)
        db.commit()
        db.refresh(db_location)
        return LocationRead.model_validate(db_location)


# Главная страница с постами
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[PostRead])
async def get_posts(skip: int = 0, limit: int = 100) -> list[PostRead]:
    with database.session() as db:
        posts = db.query(Post).offset(skip).limit(limit).all()
        return [PostRead.model_validate(p) for p in posts[::-1]]


# Посмотреть один конкретный пост
@router.get("/post/{post_id}", status_code=status.HTTP_200_OK, response_model=PostRead)
async def get_post(post_id: int) -> PostRead:
    with database.session() as db:
        post = db.query(Post).filter(Post.id == post_id).first()
        if post is None:
            raise HTTPException(status_code=404, detail="Пост не найден")
        return PostRead.model_validate(post)


# Добавить пост
@router.post("/post", status_code=status.HTTP_201_CREATED, response_model=PostRead)
async def create_post(p: PostCreate) -> PostRead:
    with database.session() as db:
        # Проверка существования связанных объектов
        db_author = db.query(User).filter(User.id == p.author_id).first()
        if not db_author:
            raise HTTPException(status_code=404, detail="Автора не существует")

        db_category = db.query(Category).filter(Category.id == p.category_id).first()
        if not db_category:
            raise HTTPException(status_code=404, detail="Категории не существует")

        db_location = db.query(Location).filter(Location.id == p.location_id).first()
        if not db_location:
            raise HTTPException(status_code=404, detail="Локации не существует")

        # Создание поста
        db_post = Post(**p.dict())
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return PostRead.model_validate(db_post)


# Изменение поста
@router.put("/post/{post_id}", status_code=status.HTTP_200_OK, response_model=PostRead)
async def update_post(post_id: int, updated_post_data: PostCreate) -> PostRead:
    with database.session() as db:
        db_post = db.query(Post).filter(Post.id == post_id).first()
        if db_post is None:
            raise HTTPException(status_code=404, detail="Пост не найден")

        # Обновление полей
        for key, value in updated_post_data.dict(exclude_unset=True).items():
            setattr(db_post, key, value)

        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return PostRead.model_validate(db_post)


# Удаление поста
@router.delete("/post/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int) -> dict:
    with database.session() as db:
        db_post = db.query(Post).filter(Post.id == post_id).first()
        if db_post is None:
            raise HTTPException(status_code=404, detail="Пост не найден")
        db.delete(db_post)
        db.commit()
        return {"text": "Пост удалён"}

#вывод всех  пользователей
@router.get("/users/", status_code=status.HTTP_200_OK, response_model=list[UserRead])
async def get_users(skip: int = 0, limit: int = 100) -> list[UserRead]:
    with database.session() as db:
        users = db.query(User).offset(skip).limit(limit).all()
        return [UserRead.model_validate(u) for u in users]
