import dataclasses
from typing import Callable
from typing import NamedTuple
from typing import Optional


class ResponseT(NamedTuple):
    status: str
    headers: dict
    payload: Optional[bytes] = None


@dataclasses.dataclass
class RequestT:
    method: str
    path: str
    headers: dict
    kwargs: Optional[dict] = None
    query: Optional[dict] = None
    form_data: Optional[dict] = None
    body: Optional[bytes] = None


HandlerT = Callable[[RequestT], ResponseT]


class StaticT(NamedTuple):
    content: bytes
    content_type: str


@dataclasses.dataclass
class UserDataT:
    name: Optional[str] = None
    address: Optional[str] = None
