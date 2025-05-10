from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from base import BaseDAO
from database import Base


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    post = relationship('Post', back_populates='group')

    def __str__(self):
        return self.title


class GroupDAO(BaseDAO):
    model = Group


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    pub_date = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey('users.id'))
    image = Column(String(255), nullable=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=True)

    author = relationship('User', back_populates='post', )
    group = relationship('Group', back_populates='post')
    comment = relationship('Comment', back_populates='post')

    def __str__(self):
        return self.text[:25]


class PostDAO(BaseDAO):
    model = Post


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))

    author = relationship('User', back_populates='comment')
    post = relationship('Post', back_populates='comment')

    def __str__(self):
        return self.text[:25]


class CommentDAO(BaseDAO):
    model = Comment
# 
