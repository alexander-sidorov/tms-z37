import os
import traceback
from contextlib import closing
from typing import Dict
from typing import List
from typing import Optional
from typing import Text

import sqlalchemy as sa
from dynaconf import settings
from fastapi import FastAPI
from pydantic.main import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI(
    description="example of API based on FastAPI and SqlAlchemy frameworks",
    title="Z37 API",
    version="1.0.0",
)

database_url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
engine = sa.create_engine(database_url)

Model = declarative_base()


class Post(Model):
    __tablename__ = "blog_post"
    id = sa.Column(sa.Integer, primary_key=True)
    author_id = sa.Column(sa.Integer)
    content = sa.Column(sa.Text)
    created_at = sa.Column(sa.DateTime)
    edited = sa.Column(sa.Boolean)
    nr_likes = sa.Column(sa.Integer)
    nr_views = sa.Column(sa.Integer)


Session = sessionmaker(bind=engine)


class MyApiResponseSchema(BaseModel):
    ok: bool = False
    errors: Optional[List[Text]] = None
    data: Optional[Dict] = None


class LikeSchema(BaseModel):
    post_id: int
    nr_likes: int


@app.get("/like/{post_id}/")
async def like(post_id: int) -> MyApiResponseSchema:
    resp = MyApiResponseSchema()

    try:
        with closing(Session()) as session:
            post = session.query(Post).filter(Post.id == post_id).first()
            if post:
                post.nr_likes += 1
                session.add(post)
                session.commit()
                like = LikeSchema(post_id=post.id, nr_likes=post.nr_likes)
                resp.ok = True
                resp.data = {"like": like}
            else:
                resp.errors = [f"post with id={post_id} was not found"]
    except Exception as err:
        resp.errors = [str(err), f"unhandled exception: {traceback.format_exc()}"]
        raise

    return resp
