from pydantic import BaseModel, SecretStr
from datetime import datetime
#класс пользователя
class User(BaseModel):
    id: int
    name: str
    password: SecretStr
#абстрактные классы, на основе которых создаются остальные
class CreatedPublishedModel(BaseModel):
    created_at: datetime
    is_published: bool
    author: User


class TitleModel(BaseModel):
    title: str

#классы на основе абстрактных
class Category(TitleModel):
    description: str


class Location(TitleModel):
    is_published: bool


class Post(CreatedPublishedModel):
    id: int
    text: str
    location: Location
    category: Category
    image: None


class Comment(CreatedPublishedModel):
    text: str
    post: Post
