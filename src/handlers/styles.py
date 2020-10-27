from framework.types import ResponseT
from framework.utils import read_static


def handle_styles(environ) -> ResponseT:
    payload = read_static("styles.css")
    status = "200 OK"
    headers = {"Content-type": "text/css"}

    return status, headers, payload
