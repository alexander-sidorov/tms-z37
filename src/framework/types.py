import dataclasses
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
    kwargs: Optional[dict] = None
