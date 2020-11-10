import dataclasses
import os
from datetime import datetime
from typing import Callable
from typing import NamedTuple
from typing import Optional

from framework.consts import DATE_TIME_FMT
from framework.consts import USER_TTL


class ResponseT(NamedTuple):
    status: str
    headers: Optional[dict] = None
    payload: Optional[bytes] = None


@dataclasses.dataclass
class RequestT:
    method: str
    path: str
    headers: dict
    kwargs: Optional[dict] = None
    body: Optional[bytes] = None
    query: Optional[dict] = None
    form_data: Optional[dict] = None
    user: Optional["UserT"] = None


HandlerT = Callable[[RequestT], ResponseT]


class StaticT(NamedTuple):
    content: bytes
    content_type: str


@dataclasses.dataclass
class UserT:
    name: Optional[str] = None
    address: Optional[str] = None
    id: Optional[str] = None
    created_at: datetime = dataclasses.field(default_factory=datetime.utcnow)

    @property
    def expired(self):
        this_moment = datetime.utcnow()
        created_at = self.created_at or this_moment
        lifetime = abs(created_at - this_moment)
        expired = lifetime >= USER_TTL
        return expired

    @staticmethod
    def dict_factory(attrs):
        processors = {
            "created_at": lambda _value: _value.strftime(DATE_TIME_FMT),
        }

        excluded_keys = {
            "id",
        }

        dct = {
            _key: processors.get(_key, lambda _value: _value)(_value)
            for _key, _value in attrs
            if _key not in excluded_keys
        }

        return dct

    def fix(self):
        if not self.id:
            self.id = os.urandom(16).hex()

        if not isinstance(self.created_at, datetime):
            self.created_at = datetime.strptime(
                self.created_at,
                DATE_TIME_FMT,
            )
