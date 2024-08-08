from datetime import datetime
from enum import Enum as PythonEnum
from sqlalchemy import Enum as SQLEnum, Integer, Column, String, DateTime, Boolean, Date, ForeignKey, \
    PrimaryKeyConstraint
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.ext.declarative import declarative_base

from utils.db import with_session

Base = declarative_base()


# Enums
class ReactionType(PythonEnum):
    LIKE = 1
    DISLIKE = -1
    HEART = 5


class ReportReason(PythonEnum):
    BREAKS_RULES = 'BREAKS_RULES'
    HARASSMENT = 'HARASSMENT'
    HATE = 'HATE'
    SHARING_PERSONAL_INFORMATION = 'SHARING_PERSONAL_INFORMATION'
    IMPERSONATION = 'IMPERSONATION'
    COPYRIGHT_VIOLATION = 'COPYRIGHT_VIOLATION'
    TRADEMARK_VIOLATION = 'TRADEMARK_VIOLATION'
    SPAM = 'SPAM'
    SELF_HARM_OR_SUICIDE = 'SELF_HARM_OR_SUICIDE'
    OTHER = 'OTHER'


# BaseModel
class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    is_deleted = Column(Boolean, default=False)

    def before_save(self, *args, **kwargs):
        pass

    @with_session
    def save(self, session):
        self.before_save()
        session.add(self)
        self.after_save()

    def after_save(self, *args, **kwargs):
        pass

    def before_update(self, *args, **kwargs):
        pass

    @with_session
    def update(self, *args, **kwargs):
        self.before_update(*args, **kwargs)
        self.after_update(*args, **kwargs)

    def after_update(self, *args, **kwargs):
        pass

    @with_session
    def delete(self, session):
        session.delete(self)


# Abstracts
class User(BaseModel):
    __tablename__ = 'users'

    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    last_login = Column(DateTime, nullable=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    display_name = Column(String(50), unique=True)
    description = Column(String(255))

    type = Column(String(15))

    __mapper_args__ = {
        'polymorphic_on': 'type',
        'polymorphic_identity': 'user'
    }


class Content(BaseModel):
    __abstract__ = True

    type = Column(String(15))

    user_id = Column(Integer, ForeignKey('users.id'))
    text = Column(String(255))

    __mapper_args__ = {
        'polymorphic_on': 'type',
        'polymorphic_identity': 'user'
    }


class FriendRequest(BaseModel):
    __tablename__ = 'friend_requests'

    approved = Column(Boolean, default=False)
    accepted_at = Column(DateTime)

    from_user_id = mapped_column(ForeignKey('users.id'))
    for_user_id = mapped_column(ForeignKey('users.id'))


class Post(Content):
    __tablename__ = 'posts'

    group_id = mapped_column(ForeignKey('groups.id'))
    group = relationship("Group", back_populates="posts")

    __mapper_args__ = {
        'polymorphic_identity': 'post'
    }


class Comment(Content):
    __tablename__ = 'comments'

    post_id = mapped_column(ForeignKey('posts.id'))
    parent_comment_id = mapped_column(ForeignKey('comments.id'), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'comment'
    }


class Group(BaseModel):
    __tablename__ = 'groups'

    name = Column(String(255), unique=True)
    description = Column(String(255))
    is_suspended = Column(Boolean, default=False)
    suspended_reason = Column(String(255))

    posts = relationship("Post", back_populates="group")


class Reaction(BaseModel):
    __tablename__ = 'reactions'

    type = Column(SQLEnum(ReactionType), name='reaction_type')
    timestamp = Column(DateTime, default='(NOW())')

    user_id = mapped_column(ForeignKey('users.id'))
    comment_id = mapped_column(ForeignKey('comments.id'), nullable=True)
    post_id = mapped_column(ForeignKey('posts.id'), nullable=True)


class GroupRequest(BaseModel):
    __tablename__ = 'group_requests'

    approved = Column(Boolean, default=False)
    at = Column(DateTime)

    user_id = mapped_column(ForeignKey('users.id'))
    group_id = mapped_column(ForeignKey('groups.id'))


class Banned(BaseModel):
    __tablename__ = 'banned'

    timestamp = Column(Date)

    user_id = mapped_column(ForeignKey('users.id'))
    administrator_id = mapped_column(ForeignKey('administrators.user_id'))
    group_administrator_id = mapped_column(ForeignKey('group_administrators.user_id'))
    group_id = mapped_column(ForeignKey('groups.id'))


class Image(BaseModel):
    __tablename__ = 'images'

    path = Column(String(255))

    user_id = mapped_column(ForeignKey('users.id'), nullable=False)
    post_id = mapped_column(ForeignKey('posts.id'), nullable=False)


class Report(BaseModel):
    __tablename__ = 'reports'

    reason = Column(SQLEnum(ReportReason), name='report_reason')
    timestamp = Column(DateTime, default='(NOW())')
    accepted = Column(Boolean)

    user_id = mapped_column(ForeignKey('users.id'), nullable=True)
    post_id = mapped_column(ForeignKey('posts.id'), nullable=True)
    comment_id = mapped_column(ForeignKey('comments.id'), nullable=True)


class Administrator(User):
    __tablename__ = 'administrators'

    user_id = mapped_column(ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'administrator'
    }


class GroupAdmin(User):
    __tablename__ = 'group_administrators'

    user_id = mapped_column(ForeignKey('users.id'), primary_key=True)
    group_id = mapped_column(ForeignKey('groups.id'), primary_key=True)

    __table_args__ = (PrimaryKeyConstraint('user_id', 'group_id'),)

    __mapper_args__ = {
        'polymorphic_identity': 'group_administrator'
    }
