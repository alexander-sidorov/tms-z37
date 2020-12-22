from fastapi import FastAPI
from fastapi import status

from api import db
from api import schemas

API_URL = "/api/v1"

app = FastAPI(
    description="example of API based on FastAPI and SqlAlchemy frameworks",
    docs_url=f"{API_URL}/docs/",
    openapi_url=f"{API_URL}/openapi.json",
    redoc_url=f"{API_URL}/redoc/",
    title="Z37 API",
    version="1.0.0",
)


@app.post(f"{API_URL}/blog/post/", status_code=status.HTTP_201_CREATED)
async def new_post(payload: schemas.NewPostApiSchema) -> schemas.PostApiSchema:
    new_post = payload.data
    obj = db.create_post(new_post)

    (obj, nr_likes) = db.get_single_post(obj.id)

    post = schemas.PostSchema(
        id=obj.id,
        author_id=obj.author_id,
        content=obj.content,
        nr_likes=nr_likes,
    )

    response = schemas.PostApiSchema(data=post)

    return response


@app.get(f"{API_URL}/blog/post/")
async def all_posts() -> schemas.PostListApiSchema:
    objects = db.get_all_posts()

    posts = [
        schemas.PostSchema(
            id=post.id,
            author_id=post.author_id,
            content=post.content,
            nr_likes=nr_likes,
        )
        for (post, nr_likes) in objects
    ]

    response = schemas.PostListApiSchema(data=posts)

    return response


@app.get(f"{API_URL}/blog/post/{{post_id}}")
async def single_post(post_id: int) -> schemas.PostApiSchema:
    response_kwargs = {}

    (obj, nr_likes) = db.get_single_post(post_id)
    if obj:
        response_kwargs["data"] = schemas.PostSchema(
            id=obj.id,
            author_id=obj.author_id,
            content=obj.content,
            nr_likes=nr_likes,
        )
    else:
        response_kwargs["errors"] = [f"post with id={post_id} does not exist"]

    response = schemas.PostApiSchema(**response_kwargs)

    return response


@app.get(f"{API_URL}/user/")
async def all_users() -> schemas.UserListApiSchema:
    objects = db.get_all_users()

    users = [
        schemas.UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
        )
        for user in objects
    ]

    response = schemas.UserListApiSchema(data=users)

    return response


@app.get(f"{API_URL}/user/{{user_id}}")
async def single_user(user_id: int) -> schemas.UserApiSchema:
    response = schemas.UserApiSchema()

    obj = db.get_single_user(user_id)
    if obj:
        response.data = schemas.UserSchema(
            id=obj.id,
            username=obj.username,
            email=obj.email,
        )
    else:
        response.errors = [f"user with id={user_id} does not exist"]

    return response


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
