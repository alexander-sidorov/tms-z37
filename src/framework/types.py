import dataclasses
from typing import Callable
from typing import NamedTuple
from typing import Optional


class ResponseT(NamedTuple):
    status: str
    headers: dict
    payload: bytes


@dataclasses.dataclass
class RequestT:
    method: str
    path: str
    headers: dict
    query: Optional[dict] = None
    kwargs: Optional[dict] = None


HandlerT = Callable[[RequestT], ResponseT]


class StaticT(NamedTuple):
    content: bytes
    content_type: str
