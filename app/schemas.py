from pydantic import BaseModel, SecretStr,ConfigDict
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    name: str
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    password: str
    name: str

class UserRead(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class CategoryBase(BaseModel):
    title: str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class LocationBase(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

class LocationCreate(LocationBase):
    pass

class LocationRead(LocationBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class PostBase(BaseModel):
    title: str
    text: str
    pub_date: Optional[datetime]
    image: Optional[str]
    model_config = ConfigDict(from_attributes=True)


class PostCreate(PostBase):
    author_id: int
    location_id: int
    category_id: int


class PostRead(PostBase):
    id: int
    author: UserRead
    location: LocationBase
    category: CategoryBase
    model_config = ConfigDict(from_attributes=True)


class CommentBase(BaseModel):
    text: str
    created_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


class CommentRead(CommentBase):
    id: int
    author: UserRead
    post_id: int
    model_config = ConfigDict(from_attributes=True)