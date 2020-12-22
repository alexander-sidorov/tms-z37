import os
from contextlib import closing
from functools import wraps
from typing import Callable
from typing import List
from typing import Optional

from delorean import now
from dynaconf import settings
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from api.schemas import PostSchema

database_url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
engine = create_engine(database_url)

Model = declarative_base()


class Post(Model):
    __tablename__ = "blog_post"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer)
    content = Column(Text)
    nr_views = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=lambda: now().datetime)
    edited = Column(Boolean, nullable=False, default=False)
    likers = relationship("BlogPostLike", backref="post")


class User(Model):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True)
    username = Column(Integer)
    email = Column(Text)

    liked_posts = relationship("BlogPostLike", backref="user")


class BlogPostLike(Model):
    __tablename__ = "blog_post_likers"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey(Post.id))
    user_id = Column(Integer, ForeignKey(User.id))


Session = sessionmaker(bind=engine)


def using_session(func: Callable):
    @wraps(func)
    def _wrapped(*args, **kwargs):
        with closing(Session()) as session:
            return func(session, *args, **kwargs)

    return _wrapped


@using_session
def create_post(session: Session, data: PostSchema) -> Post:
    post = Post(
        author_id=data.author_id,
        content=data.content,
    )
    session.add(post)
    session.commit()

    session.refresh(post)

    return post


@using_session
def get_all_posts(session: Session) -> List[Post]:
    result = (
        session.query(Post, func.count(BlogPostLike.id).label("nr_likes"))
        .outerjoin(Post.likers)
        .group_by(Post.id)
        .all()
    )
    return list(result)


@using_session
def get_single_post(session: Session, post_id: int) -> Optional[Post]:
    result = (
        session.query(Post, func.count(BlogPostLike.id).label("nr_likes"))
        .outerjoin(Post.likers)
        .filter(Post.id == post_id)
        .group_by(Post.id)
        .first()
    )
    return result or (None, None)


@using_session
def get_all_users(session: Session) -> List[User]:
    result = session.query(User).all()
    return list(result)


@using_session
def get_single_user(session: Session, user_id: int) -> Optional[User]:
    result = session.query(User).filter(User.id == user_id).first()
    return result
