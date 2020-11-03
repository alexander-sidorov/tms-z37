import traceback

from framework.types import RequestT
from framework.types import ResponseT


def handle_500(_request: RequestT = None) -> ResponseT:
    document = traceback.format_exc()

    payload = document.encode()
    status = "500 Internal Server Error"
    headers = {"Content-type": "text/plain"}

    return ResponseT(status, headers, payload)
