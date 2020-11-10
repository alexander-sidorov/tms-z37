from framework.types import RequestT
from framework.types import ResponseT
from framework.types import UserDataT
from framework.utils import build_status
from framework.utils import load_user_data
from framework.utils import read_static
from framework.utils import save_user_data


def handle_hello(request: RequestT) -> ResponseT:
    if request.method == "GET":
        return handle_hello_get(request)
    else:
        return handle_hello_post(request)


def handle_hello_get(request: RequestT) -> ResponseT:
    assert request.method == "GET"

    base = read_static("_base.html")
    base_html = base.content.decode()
    hello_html = read_static("hello.html").content.decode()

    user_data = load_user_data()

    document = hello_html.format(
        address_header=user_data.address or "nowhere",
        address_value=user_data.address or "",
        name_header=user_data.name or "anon",
        name_value=user_data.name or "",
    )
    document = base_html.format(xxx=document)

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

    user_data = UserDataT(name=name, address=address)

    save_user_data(user_data)

    response = ResponseT(
        status=build_status(302),
        headers={"Location": "/h/"},
    )

    return response
