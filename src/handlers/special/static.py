from framework.types import RequestT
from framework.types import ResponseT


def handle_static(request: RequestT) -> ResponseT:
    path = request.path
    return ResponseT("200 OK", {}, path.encode())
