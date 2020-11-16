import http
import mimetypes
import re
from html import escape
from http.cookies import SimpleCookie
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Tuple
from urllib.parse import parse_qs

from framework import settings
from framework.consts import DIR_STATIC
from framework.consts import METHODS_WITH_REQUEST_BODY
from framework.consts import USER_COOKIE
from framework.consts import USER_TTL
from framework.db import find_user
from framework.errors import NotFound
from framework.types import RequestT
from framework.types import StaticT
from framework.types import UserT

HeaderTupleT = Tuple[str, Any]


def http_first(value: HeaderTupleT) -> Tuple[int, HeaderTupleT]:
    """
    Key function for `sorted`.
    Orders a header tuple such that
    the header which starts with HTTP_ will be assigned a value 0,
    meaning that the tuple will be the first
    when under sorting by function `sorted`, or kind of.

    :param value: header tuple (name, value)
    :return: ordered header (int, (name, value))
    """

    order = 0 if value[0].startswith("HTTP") else 1
    return order, value


def format_env_var(name: str, value: str) -> str:
    """
    Formats environment variable value.
    Formatter is chosen according to the kind of variable.

    :param name: name of environment variable
    :param value: value of environment variable
    :return: string representation of value in appropriate format
    """

    formatter = get_formatter(name)
    new = str(value)
    new = formatter(new)
    new = escape(new)
    new = re.sub("\n", "<br>", new)

    return new


def get_formatter(env_var_name: str) -> Callable[[str], str]:
    """
    Returns a formatter function for given environment variablel.

    :param env_var_name: name of environment variable
    :return: formatting function
    """

    if env_var_name.endswith("PATH"):
        return lambda _value: "\n".join(_value.split(":"))

    if "ACCEPT" in env_var_name:
        return lambda _v: "\n".join(re.split(r"[\s,]+", _v))

    return lambda _v: _v


def read_static(file_name: str) -> StaticT:
    """
    Reads the content of the static file from given path.
    If file name is in relative form, reads data from static dir.
    If file name is in absolute form, reads data from the file itself.

    :param file_name: path to the file
    :return: content and content type
    """

    if file_name.startswith("/"):  # TODO: enhance to support Windows
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
    """
    Returns request headers from WSGI environment.
    Headers names are adopted: "HTTP_" part is cut of.

    :param environ: WSGI environ
    :return: dict with HTTP headers
    """

    environ_headers = filter(lambda _kv: _kv[0].startswith("HTTP_"), environ.items())
    request_headers = {key[5:]: value for key, value in environ_headers}
    return request_headers


def get_request_query(environ: dict) -> dict:
    """
    Returns parsed query from WSGI environ.
    Returns empty dict if no query provided in HTTP request.

    :param environ: WSGI environ
    :return: dict with query params
    """

    qs = environ.get("QUERY_STRING")
    query = parse_qs(qs or "")
    return query


def build_status(code: int) -> str:
    """
    Builds a string with HTTP status code and reason for given code.

    :param code: integer HTTP code
    :return: string with code and reason
    """

    status = http.HTTPStatus(code)

    def _process_word(_word: str) -> str:
        if _word == "OK":
            return _word
        return _word.capitalize()

    reason = " ".join(_process_word(word) for word in status.name.split("_"))

    text = f"{code} {reason}"
    return text


def build_form_data(body: bytes) -> Dict[str, Any]:
    """
    Builds a dict with form names&values against request body.
    Returns empty dict if request body is empty.

    :param body: HTTP request body
    :return: dict with form data
    """

    if not body:
        return {}

    qs = body.decode()
    form_data = parse_qs(qs or "")
    return form_data


def get_request_body(environ: dict) -> Optional[bytes]:
    """
    Returns a HTTP request body against given WSGI environment.
    Returns None if it is impossible to obtain a request body.

    :param environ: WSGI environment
    :return: bytes of HTTP request body or None
    """

    method = get_request_method(environ)
    if method not in METHODS_WITH_REQUEST_BODY:
        return None

    fp = environ.get("wsgi.input")
    if not fp:
        return None

    content_length = int(environ.get("CONTENT_LENGTH") or 0)
    if not content_length:
        return None

    content = fp.read(content_length)

    return content


def get_request_method(environ: dict) -> str:
    """
    Returns a method name of HTTP request.

    :param environ: WSGI environment
    :return: HTTP method name
    """

    method = environ["REQUEST_METHOD"]
    return method


def get_request_path(environ: dict) -> str:
    """
    Returns a path part of the HTTP request.

    :param environ: WSGI environment
    :return: request path
    """

    path = environ["PATH_INFO"]
    return path


def build_cookies(headers: Dict) -> SimpleCookie:
    """
    Builds a cookies jar against given headers.

    :param headers: dict with HTTP request headers
    :return: SimpleCookie jar
    """

    cookies = SimpleCookie(headers.get("COOKIE", ""))
    return cookies


def authenticate(request: RequestT) -> None:
    """
    Sets an user up in the given request.

    :param request: HTTP request
    """

    request.user = UserT()

    if USER_COOKIE not in request.cookies:
        return

    user_id = request.cookies[USER_COOKIE].value
    user = find_user(user_id)
    request.user = user


def _build_session_header_generic(user_id, max_age):
    """
    Builds a generic header value for user session.

    :param user_id: user ID
    :param max_age: Max-Age value of cookie
    :return: session header
    """

    jar = SimpleCookie()

    jar[USER_COOKIE] = user_id

    cookie = jar[USER_COOKIE]
    cookie["Domain"] = settings.HOST
    cookie["HttpOnly"] = True
    cookie["Max-Age"] = max_age
    cookie["Path"] = "/"

    header = jar.output(header="").strip()
    return header


def build_session_header(user_id: str) -> str:
    """
    Builds a header value for user session.

    :param user_id: user ID
    :return: session header
    """

    return _build_session_header_generic(user_id, USER_TTL.total_seconds())


def build_reset_session_header(user_id: str) -> str:
    """
    Builds a reset header value for user session.

    :param user_id: user ID
    :return: session header
    """

    return _build_session_header_generic(user_id, 0)


def host_is_local(host: str) -> bool:
    """
    Tells whether given host is local.

    :param host: host name or address
    :return: True if host is local otherwise False
    """

    local_names = {
        "localhost",
        "127.0.0.1",
    }

    is_local = any(local_name in host for local_name in local_names)
    return is_local


def build_absolute_url(resource: str, **kwargs: dict) -> str:
    """
    Builds an absolute URL to given resource according to the active host.

    :param resource: name of the resource (path)
    :param kwargs: kwargs part of the URL
    :return: an absolute URL
    """

    port = settings.PORT
    if port in (80, 443):
        port = ""
    else:
        port = f":{port}"

    host = settings.HOST

    schema = "http" if host_is_local(host) else "https"

    if resource.startswith("/"):
        resource = resource[1:]

    url = f"{schema}://{host}{port}/{resource}"
    if kwargs:
        url = url.format(**kwargs)

    return url
