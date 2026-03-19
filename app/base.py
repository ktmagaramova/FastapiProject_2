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

#пользователь
@router.post("/user/", status_code=status.HTTP_201_CREATED, response_model=UserRead)
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


@router.get("/users/", status_code=status.HTTP_200_OK, response_model=list[UserRead])
async def get_users(skip: int = 0, limit: int = 100) -> list[UserRead]:
    with database.session() as db:
        users = db.query(User).offset(skip).limit(limit).all()
        return [UserRead.model_validate(u) for u in users]


@router.get("/user/{user_id}", status_code=status.HTTP_200_OK, response_model=UserRead)
async def get_user(user_id: int) -> UserRead:
    with database.session() as db:
        user = db.query(User).filter(User.id == user_id).first()
        return UserRead.model_validate(user)


@router.put("/user/{user_id}", status_code=status.HTTP_200_OK, response_model=UserRead)
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


@router.delete("/user/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int) -> dict:
    with database.session() as db:
        db_user = db.query(User).filter(User.id == user_id).first()
        db.delete(db_user)
        db.commit()
        return {"detail": "Пользователь удалён"}


# категории
@router.post("/categorie/", status_code=status.HTTP_201_CREATED, response_model=CategoryRead)
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


@router.get("/categories/", status_code=status.HTTP_200_OK, response_model=list[CategoryRead])
async def get_categories(skip: int = 0, limit: int = 100) -> list[CategoryRead]:
    with database.session() as db:
        categories = db.query(Category).offset(skip).limit(limit).all()
        return [CategoryRead.model_validate(c) for c in categories]


@router.get("/categorie/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryRead)
async def get_category(category_id: int) -> CategoryRead:
    with database.session() as db:
        category = db.query(Category).filter(Category.id == category_id).first()
        return CategoryRead.model_validate(category)


@router.put("/categorie/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryRead)
async def update_category(category_id: int, category_data: CategoryCreate) -> CategoryRead:
    with database.session() as db:
        db_category = db.query(Category).filter(Category.id == category_id).first()
        db_category.title = category_data.title
        db_category.description = category_data.description or ""
        db_category.slug = category_data.slug or ""
        db.commit()
        db.refresh(db_category)
        return CategoryRead.model_validate(db_category)


@router.delete("/categorie/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: int) -> dict:
    with database.session() as db:
        db_category = db.query(Category).filter(Category.id == category_id).first()
        db.delete(db_category)
        db.commit()
        return {"detail": "Категория удалена"}


#локация
@router.post("/location/", status_code=status.HTTP_201_CREATED, response_model=LocationRead)
def create_location(l: LocationCreate) -> LocationRead:
    with database.session() as db:
        db_location = Location(
            name=l.name,
            is_published=True,
            created_at=datetime.utcnow()
        )
        db.add(db_location)
        db.commit()
        db.refresh(db_location)
        return LocationRead.model_validate(db_location)


@router.get("/locations/", status_code=status.HTTP_200_OK, response_model=list[LocationRead])
async def get_locations(skip: int = 0, limit: int = 100) -> list[LocationRead]:
    with database.session() as db:
        locations = db.query(Location).offset(skip).limit(limit).all()
        return [LocationRead.model_validate(l) for l in locations]


@router.get("/location/{location_id}", status_code=status.HTTP_200_OK, response_model=LocationRead)
async def get_location(location_id: int) -> LocationRead:
    with database.session() as db:
        location = db.query(Location).filter(Location.id == location_id).first()
        return LocationRead.model_validate(location)


@router.put("/location/{location_id}", status_code=status.HTTP_200_OK, response_model=LocationRead)
async def update_location(location_id: int, location_data: LocationCreate) -> LocationRead:
    with database.session() as db:
        db_location = db.query(Location).filter(Location.id == location_id).first()
        db_location.name = location_data.name
        db.commit()
        db.refresh(db_location)
        return LocationRead.model_validate(db_location)


@router.delete("/location/{location_id}", status_code=status.HTTP_200_OK)
async def delete_location(location_id: int) -> dict:
    with database.session() as db:
        db_location = db.query(Location).filter(Location.id == location_id).first()
        db.delete(db_location)
        db.commit()
        return {"detail": "Локация удалена"}


#посты
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[PostRead])
async def get_posts(skip: int = 0, limit: int = 100) -> list[PostRead]:
    with database.session() as db:
        posts = db.query(Post).offset(skip).limit(limit).all()
        return [PostRead.model_validate(p) for p in posts[::-1]]


@router.get("/post/{post_id}", status_code=status.HTTP_200_OK, response_model=PostRead)
async def get_post(post_id: int) -> PostRead:
    with database.session() as db:
        post = db.query(Post).filter(Post.id == post_id).first()
        return PostRead.model_validate(post)


@router.post("/post", status_code=status.HTTP_201_CREATED, response_model=PostRead)
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


@router.put("/post/{post_id}", status_code=status.HTTP_200_OK, response_model=PostRead)
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


@router.delete("/post/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int) -> dict:
    with database.session() as db:
        db_post = db.query(Post).filter(Post.id == post_id).first()
        db.delete(db_post)
        db.commit()
        return {"detail": "Пост удалён"}


#комменты

@router.post("/comment/", status_code=status.HTTP_201_CREATED, response_model=CommentRead)
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


@router.get("/comments/", status_code=status.HTTP_200_OK, response_model=list[CommentRead])
async def get_comments(skip: int = 0, limit: int = 100) -> list[CommentRead]:
    with database.session() as db:
        comments = db.query(Comment).offset(skip).limit(limit).all()
        return [CommentRead.model_validate(c) for c in comments]


@router.get("/post/{post_id}/comments", status_code=status.HTTP_200_OK, response_model=list[CommentRead])
async def get_post_comments(post_id: int, skip: int = 0, limit: int = 100) -> list[CommentRead]:
    with database.session() as db:
        comments = db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()
        return [CommentRead.model_validate(c) for c in comments]


@router.delete("/comment/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment(comment_id: int) -> dict:
    with database.session() as db:
        db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
        db.delete(db_comment)
        db.commit()
        return {"detail": "Комментарий удалён"}