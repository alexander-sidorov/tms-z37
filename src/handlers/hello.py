from framework import settings
from framework.consts import USER_COOKIE
from framework.consts import USER_TTL
from framework.db import save_user
from framework.errors import MethodNotAllowed
from framework.types import RequestT
from framework.types import ResponseT
from framework.utils import build_status
from framework.utils import read_static


def handle_hello(request: RequestT) -> ResponseT:
    handlers = {
        "GET": handle_hello_get,
        "POST": handle_hello_post,
    }

    handler = handlers.get(request.method)
    if not handler:
        raise MethodNotAllowed

    response = handler(request)
    return response


def handle_hello_get(request: RequestT) -> ResponseT:
    assert request.method == "GET"

    base = read_static("_base.html")
    base_html = base.content.decode()
    hello_html = read_static("hello.html").content.decode()

    document = hello_html.format(
        address_header=request.user.address or "nowhere",
        address_value=request.user.address or "",
        name_header=request.user.name or "anon",
        name_value=request.user.name or "",
    )
    document = base_html.format(body=document)

    resp = ResponseT(
        status=build_status(200),
        headers={"Content-Type": base.content_type},
        payload=document.encode(),
    )

    return resp


def handle_hello_post(request: RequestT) -> ResponseT:
    assert request.method == "POST"

    form_data = request.form_data

    name = form_data.get("name", [None])[0]
    address = form_data.get("address", [None])[0]

    request.user.name = name
    request.user.address = address

    save_user(request.user)

    status = build_status(302)
    headers = {
        "Location": "/h/",
        "Set-Cookie": (
            f"{USER_COOKIE}={request.user.id};"
            f" Domain={settings.HOST};"
            f" HttpOnly;"
            f" Max-Age={USER_TTL.total_seconds()}"
        ),
    }

    response = ResponseT(
        headers=headers,
        status=status,
    )

    return response
