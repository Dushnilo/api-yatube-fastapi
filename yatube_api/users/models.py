from sqlalchemy import (Column, DateTime, Integer, String, ForeignKey,
                        UniqueConstraint)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from base import BaseDAO
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    username = Column(String, unique=True, index=True)
    date_joined = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    role = Column(String, default='user')
    first_name = Column(String, index=True, nullable=True)
    last_name = Column(String, index=True, nullable=True)

    post = relationship('Post', back_populates='author')
    comment = relationship('Comment', back_populates='author')
    follower = relationship('Follow', back_populates='follower_user',
                            foreign_keys='Follow.user_id')
    following = relationship('Follow', back_populates='following_user',
                             foreign_keys='Follow.following_id')

    def __str__(self):
        return self.username


class UsersDAO(BaseDAO):
    model = User


class Follow(Base):
    __tablename__ = 'follows'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    following_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    follower_user = relationship('User', foreign_keys=[user_id],
                                 back_populates='follower')
    following_user = relationship('User', foreign_keys=[following_id],
                                  back_populates='following')

    __table_args__ = (UniqueConstraint('user_id', 'following_id',
                                       name='unique_follow'),)


class FollowDAO(BaseDAO):
    model = Follow
