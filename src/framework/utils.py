import http
import mimetypes
import re
from html import escape
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import Tuple
from urllib.parse import parse_qs

from framework.consts import DIR_STATIC
from framework.consts import METHODS_WITH_REQUEST_BODY
from framework.errors import NotFound
from framework.types import StaticT


def http_first(value: Tuple[str, Any]) -> tuple:
    if value[0].startswith("HTTP"):
        return 0, value
    return 1, value


def format_env_var(name: str, value: str) -> str:
    formatter = get_formatter(name)
    new = str(value)
    new = formatter(new)
    new = escape(new)
    new = re.sub("\n", "<br>", new)

    return new


def get_formatter(env_var_name: str) -> Callable[[str], str]:
    if env_var_name.endswith("PATH"):
        return lambda _value: "\n".join(_value.split(":"))
    if "ACCEPT" in env_var_name:
        return lambda _v: "\n".join(re.split(r"[\s,]+", _v))
    return lambda _v: _v


def read_static(file_name: str) -> StaticT:
    if file_name.startswith("/"):
        file_obj = Path(file_name).resolve()
    else:
        file_obj = (DIR_STATIC / file_name).resolve()

    if not file_obj.exists():
        raise NotFound

    with file_obj.open("rb") as fp:
        content = fp.read()

    content_type = mimetypes.guess_type(file_name)[0]

    return StaticT(content=content, content_type=content_type)


def get_request_headers(environ: dict) -> dict:
    environ_headers = filter(lambda _kv: _kv[0].startswith("HTTP_"), environ.items())
    request_headers = {key[5:]: value for key, value in environ_headers}
    return request_headers


def get_request_query(environ: dict) -> dict:
    qs = environ.get("QUERY_STRING")
    query = parse_qs(qs or "")
    return query


def build_status(code: int) -> str:
    status = http.HTTPStatus(code)

    def _process_word(_word: str) -> str:
        if _word == "OK":
            return _word
        return _word.capitalize()

    reason = " ".join(_process_word(word) for word in status.name.split("_"))

    text = f"{code} {reason}"
    return text


def build_form_data(body: bytes) -> Dict[str, Any]:
    qs = body.decode()
    form_data = parse_qs(qs or "")
    return form_data


def get_request_body(environ: dict) -> bytes:
    method = get_request_method(environ)
    if method not in METHODS_WITH_REQUEST_BODY:
        return b""

    fp = environ.get("wsgi.input")
    if not fp:
        return b""

    cl = int(environ.get("CONTENT_LENGTH") or 0)
    if not cl:
        return b""

    content = fp.read(cl)

    return content


def get_request_method(environ: dict) -> str:
    method = environ.get("REQUEST_METHOD", "GET")
    return method


def get_request_path(environ: dict) -> str:
    path = environ.get("PATH_INFO", "/")
    return path
