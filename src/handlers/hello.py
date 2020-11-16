from framework.db import delete_user
from framework.db import save_user
from framework.errors import MethodNotAllowed
from framework.errors import NotFound
from framework.types import RequestT
from framework.types import ResponseT
from framework.utils import build_reset_session_header
from framework.utils import build_session_header
from framework.utils import build_status
from framework.utils import read_static


def handle_hello(request: RequestT) -> ResponseT:
    handlers = {
        "greet": _handle_hello_greet,
        "reset": _handle_hello_reset,
    }

    handler = handlers.get(request.kwargs.get("action"), _handle_hello_index)
    if not handler:
        raise NotFound

    response = handler(request)
    return response


def _handle_hello_index(request: RequestT) -> ResponseT:
    if request.method != "GET":
        raise MethodNotAllowed

    base = read_static("_base.html")
    base_html = base.content.decode()
    hello_html = read_static("hello.html").content.decode()

    body = hello_html.format(
        address_header=request.user.address or "the middle of fucking nowhere",
        address_value=request.user.address or "",
        name_header=request.user.name or "anonymous",
        name_value=request.user.name or "",
    )

    document = base_html.format(body=body)

    status = build_status(200)

    headers = {"Content-Type": base.content_type}

    response = ResponseT(
        headers=headers,
        payload=document.encode(),
        status=status,
    )

    return response


def _handle_hello_greet(request: RequestT) -> ResponseT:
    if request.method != "POST":
        raise MethodNotAllowed

    name = request.form_data.get("name", [None])[0]
    address = request.form_data.get("address", [None])[0]

    request.user.name = name
    request.user.address = address

    save_user(request.user)

    status = build_status(302)

    cookie = build_session_header(request.user.id)

    headers = {
        "Location": "/h/",
        "Set-Cookie": cookie,
    }

    response = ResponseT(
        headers=headers,
        status=status,
    )

    return response


def _handle_hello_reset(request: RequestT) -> ResponseT:
    if request.method != "POST":
        raise MethodNotAllowed

    delete_user(request.user)

    status = build_status(302)

    cookie = build_reset_session_header(request.user.id)

    headers = {
        "Location": "/h/",
        "Set-Cookie": cookie,
    }

    response = ResponseT(
        headers=headers,
        status=status,
    )

    return response
