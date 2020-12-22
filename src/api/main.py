from dynaconf import settings
from fastapi import FastAPI
from fastapi import status

from api import db
from api import schemas
from framework.logging_for_humans import configure_logging

API_URL = "/api/v1"

app = FastAPI(
    description="example of API based on FastAPI and SqlAlchemy frameworks",
    docs_url=f"{API_URL}/docs/",
    openapi_url=f"{API_URL}/openapi.json",
    redoc_url=f"{API_URL}/redoc/",
    title="Z37 API",
    version="1.0.0",
)

logger = configure_logging("api")


@app.post(f"{API_URL}/blog/post/", status_code=status.HTTP_201_CREATED)
async def new_post(payload: schemas.PostApiSchema) -> schemas.PostApiSchema:
    logger.debug("creating new post")

    new_post = payload.data
    logger.debug(f"payload: {payload}")

    obj = db.create_post(new_post)
    logger.debug(f"created obj: {obj}")

    (obj, nr_likes) = db.get_single_post(obj.id)
    logger.debug(f"read obj: {obj}, nr_likes: {nr_likes}")

    post = schemas.PostSchema(
        id=obj.id,
        author_id=obj.author_id,
        content=obj.content,
        nr_likes=str(nr_likes),
    )
    logger.debug(f"built post: {post}")

    response = schemas.PostApiSchema(data=post)
    logger.debug(f"built response: {response}")

    return response


@app.get(f"{API_URL}/blog/post/")
async def all_posts() -> schemas.PostListApiSchema:
    logger.debug("retrieving all posts")

    objects = db.get_all_posts()
    logger.debug(f"all posts ids: {[obj.id for (obj, _) in objects]}")

    posts = [
        schemas.PostSchema(
            id=post.id,
            author_id=post.author_id,
            content=post.content,
            nr_likes=nr_likes,
        )
        for (post, nr_likes) in objects
    ]
    logger.debug("built posts")

    response = schemas.PostListApiSchema(data=posts)
    logger.debug("built response")

    return response


@app.get(f"{API_URL}/blog/post/{{post_id}}")
async def single_post(post_id: int) -> schemas.PostApiSchema:
    logger.debug(f"retrieving a single post, id={post_id}")

    response_kwargs = {}

    (obj, nr_likes) = db.get_single_post(post_id)
    logger.debug(f"got post obj: {obj}, nr_likes: {nr_likes}")

    if obj:
        logger.debug("post found, building schema obj")

        response_kwargs["data"] = schemas.PostSchema(
            id=obj.id,
            author_id=obj.author_id,
            content=obj.content,
            nr_likes=nr_likes,
        )
    else:
        logger.debug("post found, building error description")

        response_kwargs["errors"] = [f"post with id={post_id} does not exist"]

    response = schemas.PostApiSchema(**response_kwargs)
    logger.debug("build response")

    return response


@app.get(f"{API_URL}/user/")
async def all_users() -> schemas.UserListApiSchema:
    logger.debug("retrieving all users")

    objects = db.get_all_users()
    logger.debug(f"all users ids: {[obj.id for obj in objects]}")

    users = [
        schemas.UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
        )
        for user in objects
    ]
    logger.debug("built users")

    response = schemas.UserListApiSchema(data=users)
    logger.debug("build response")

    return response


@app.get(f"{API_URL}/user/{{user_id}}")
async def single_user(user_id: int) -> schemas.UserApiSchema:
    logger.debug(f"retrieving a single user, id={user_id}")

    response_kwargs = {}

    obj = db.get_single_user(user_id)
    logger.debug(f"got user obj: {obj}")

    if obj:
        logger.debug("post found, building schema obj")

        response_kwargs["data"] = schemas.UserSchema(
            id=obj.id,
            username=obj.username,
            email=obj.email,
        )
    else:
        logger.debug("post found, building error description")

        response_kwargs["errors"] = [f"user with id={user_id} does not exist"]

    response = schemas.UserApiSchema(**response_kwargs)
    logger.debug("build response")

    return response


if __name__ == "__main__" and settings.MODE_DEBUG:
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
