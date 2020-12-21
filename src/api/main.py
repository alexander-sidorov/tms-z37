from fastapi import FastAPI
from fastapi import status

from api.db import create_post
from api.db import get_all_posts
from api.db import get_all_users
from api.db import get_single_post
from api.db import get_single_user
from api.schemas import JsonApiResponseSchema
from api.schemas import NewPostSchema
from api.schemas import PostSchema
from api.schemas import UserSchema

app = FastAPI(
    description="example of API based on FastAPI and SqlAlchemy frameworks",
    title="Z37 API",
    version="1.0.0",
)

API_URL = "/api/v1"


@app.post(f"{API_URL}/post/", status_code=status.HTTP_201_CREATED)
async def new_post(post: NewPostSchema) -> JsonApiResponseSchema:
    obj = create_post(post)
    (obj, nr_likes) = get_single_post(obj.id)
    payload = PostSchema(
        id=obj.id,
        author_id=obj.author_id,
        content=obj.content,
        nr_likes=nr_likes,
    )
    resp = JsonApiResponseSchema(data=payload)
    return resp


@app.get(f"{API_URL}/post/")
async def all_posts() -> JsonApiResponseSchema:
    posts = get_all_posts()
    payload = [
        PostSchema(
            id=post.id,
            author_id=post.author_id,
            content=post.content,
            nr_likes=nr_likes,
        )
        for (post, nr_likes) in posts
    ]
    resp = JsonApiResponseSchema(data=payload)
    return resp


@app.get(f"{API_URL}/post/{{post_id}}")
async def single_post(post_id: int) -> JsonApiResponseSchema:
    resp = JsonApiResponseSchema()
    (post, nr_likes) = get_single_post(post_id)
    if post:
        resp.data = PostSchema(
            id=post.id,
            author_id=post.author_id,
            content=post.content,
            nr_likes=nr_likes,
        )
    else:
        resp.errors = [f"no post found with id={post_id}"]
    return resp


@app.get(f"{API_URL}/user/")
async def all_users() -> JsonApiResponseSchema:
    users = get_all_users()
    payload = [
        UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
        )
        for user in users
    ]
    resp = JsonApiResponseSchema(data=payload)
    return resp


@app.get(f"{API_URL}/user/{{user_id}}")
async def single_user(user_id: int) -> JsonApiResponseSchema:
    resp = JsonApiResponseSchema()
    user = get_single_user(user_id)
    if user:
        resp.data = UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
        )
    else:
        resp.errors = [f"no user found with id={user_id}"]
    return resp


"""async def like(post_id: int) -> MyApiResponseSchema:
    resp = MyApiResponseSchema()

    try:
        with closing(Session()) as session:
            # post = session.query(Post).filter(Post.id == post_id).first()
            if 1:
                # post.nr_likes += 1
                # session.add(post)
                # session.commit()
                like = LikeSchema(post_id=post_id, nr_likes=1)
                resp.ok = True
                resp.data = {"like": like}
            else:
                resp.errors = [f"post with id={post_id} was not found"]
    except Exception as err:
        resp.errors = [str(err), f"unhandled exception: {traceback.format_exc()}"]
        raise

    return resp"""
