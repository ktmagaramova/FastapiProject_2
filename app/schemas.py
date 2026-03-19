from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = ""
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""


class UserRead(BaseModel):
    id: int
    username: str
    email: Optional[str] = ""
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    is_active: bool = True
    model_config = ConfigDict(from_attributes=True)

class CategoryCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    slug: Optional[str] = None


class CategoryRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = ""
    is_published: bool = True
    created_at: Optional[datetime] = None
    slug: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class LocationCreate(BaseModel):
    name: str


class LocationRead(BaseModel):
    id: int
    name: str
    is_published: bool = True
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class PostCreate(BaseModel):
    title: str
    text: str
    pub_date: datetime
    author_id: int
    category_id: Optional[int] = None
    location_id: Optional[int] = None
    image: Optional[str] = None


class PostUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    pub_date: Optional[datetime] = None
    image: Optional[str] = None
    category_id: Optional[int] = None
    location_id: Optional[int] = None


class PostRead(BaseModel):
    id: int
    title: str
    text: str
    pub_date: datetime
    is_published: bool = True
    created_at: Optional[datetime] = None
    image: Optional[str] = None
    author: UserRead
    category: Optional[CategoryRead] = None
    location: Optional[LocationRead] = None
    model_config = ConfigDict(from_attributes=True)


class CommentCreate(BaseModel):
    text: str
    post_id: int
    author_id: int


class CommentRead(BaseModel):
    id: int
    text: str
    created_at: Optional[datetime] = None
    is_published: bool = True
    author: UserRead
    post_id: int
    model_config = ConfigDict(from_attributes=True)