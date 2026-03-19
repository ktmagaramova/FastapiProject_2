from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class User(Base):
    __tablename__ = 'auth_user'

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime, nullable=True)
    is_superuser = Column(Boolean, default=False)
    username = Column(String(150), unique=True, index=True, nullable=False)
    first_name = Column(String(150), nullable=False, default="")
    last_name = Column(String(150), nullable=False, default="")
    email = Column(String(254), nullable=False, default="")
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    date_joined = Column(DateTime, nullable=False, default=datetime.utcnow)

    posts = relationship('Post', back_populates='author', foreign_keys='Post.author_id',
                         primaryjoin='User.id==Post.author_id')
    comments = relationship('Comment', back_populates='author', foreign_keys='Comment.author_id',
                            primaryjoin='User.id==Comment.author_id')


class Category(Base):
    __tablename__ = 'blog_category'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    is_published = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    slug = Column(String(255), nullable=True)

    posts = relationship('Post', back_populates='category', foreign_keys='Post.category_id',
                         primaryjoin='Category.id==Post.category_id')


class Location(Base):
    __tablename__ = 'blog_location'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    is_published = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    posts = relationship('Post', back_populates='location', foreign_keys='Post.location_id',
                         primaryjoin='Location.id==Post.location_id')


class Post(Base):
    __tablename__ = 'blog_post'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)
    pub_date = Column(DateTime, nullable=False)
    is_published = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    image = Column(String(100), nullable=True)

    author_id = Column(Integer, ForeignKey('auth_user.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('blog_category.id'), nullable=True)
    location_id = Column(Integer, ForeignKey('blog_location.id'), nullable=True)

    author = relationship("User", back_populates="posts", foreign_keys=[author_id])
    category = relationship("Category", back_populates="posts", foreign_keys=[category_id])
    location = relationship("Location", back_populates="posts", foreign_keys=[location_id])
    comments = relationship("Comment", back_populates="post", foreign_keys='Comment.post_id',
                            primaryjoin='Post.id==Comment.post_id')


class Comment(Base):
    __tablename__ = 'blog_comment'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    is_published = Column(Boolean, nullable=False, default=True)
    text = Column(Text, nullable=False)

    author_id = Column(Integer, ForeignKey('auth_user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('blog_post.id'), nullable=False)

    author = relationship("User", back_populates="comments", foreign_keys=[author_id])
    post = relationship("Post", back_populates="comments", foreign_keys=[post_id])