from typing import Dict
from typing import Optional

from fastapi import FastAPI
from pydantic.main import BaseModel

app = FastAPI(
    description="example of API based on FastAPI and SqlAlchemy frameworks",
    title="Z37 API",
    version="1.0.0",
)


class MyApiResponseSchema(BaseModel):
    ok: bool = False
    errors: Optional[Dict] = None
    data: Optional[Dict] = None


class LikeSchema(BaseModel):
    post_id: int
    nr_likes: int


@app.get("/like/{post_id}/")
async def like(post_id: int) -> MyApiResponseSchema:
    like = LikeSchema(post_id=post_id, nr_likes=-1)
    resp = MyApiResponseSchema(ok=True, data={"like": like})

    return resp
