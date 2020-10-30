from typing import NamedTuple


class ResponseT(NamedTuple):
    status: str
    headers: dict
    payload: bytes
