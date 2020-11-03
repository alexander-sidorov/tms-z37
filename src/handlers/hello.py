from framework.types import RequestT
from framework.types import ResponseT
from framework.utils import build_status
from framework.utils import read_static


def handle_hello(request: RequestT) -> ResponseT:
    name = (request.query.get("name") or ["anon"])[0]

    base = read_static("_base.html")
    base_html = base.content.decode()
    document = base_html.format(xxx=f"<h2>hello {name}</h2>")

    resp = ResponseT(
        status=build_status(200),
        headers={"Content-Type": base.content_type},
        payload=document.encode(),
    )
    return resp
