from typing import Dict
from typing import List
from typing import Optional
from typing import Text
from typing import Union

from pydantic.main import BaseModel


class JsonApiSchema(BaseModel):
    errors: Optional[List[Text]] = None
    data: Union[List, Optional[Dict]] = None


class UserSchema(BaseModel):
    id: int
    username: str
    email: str


UserListSchema = List[UserSchema]


class PostSchema(BaseModel):
    author_id: int
    content: str
    id: Optional[int] = None
    nr_likes: Optional[int] = 0


PostListSchema = List[PostSchema]


class UserListApiSchema(JsonApiSchema):
    data: UserListSchema


class UserApiSchema(JsonApiSchema):
    data: UserSchema


class PostListApiSchema(JsonApiSchema):
    data: PostListSchema


class PostApiSchema(JsonApiSchema):
    data: PostSchema
