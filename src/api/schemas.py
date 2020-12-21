from typing import Dict
from typing import List
from typing import Optional
from typing import Text
from typing import Union

from pydantic.main import BaseModel


class JsonApiResponseSchema(BaseModel):
    errors: Optional[List[Text]] = None
    data: Union[Optional[Dict], List] = None


class UserSchema(BaseModel):
    id: int
    username: str
    email: str


class NewPostSchema(BaseModel):
    author_id: int
    content: str


class PostSchema(NewPostSchema):
    id: int
    nr_likes: int
