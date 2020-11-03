import mimetypes
from pathlib import Path

from framework.types import RequestT
from framework.types import ResponseT
from framework.utils import read_static


def handle_static(request: RequestT) -> ResponseT:
    path = request.path
    file_name = request.kwargs["file_name"]
    content_type = mimetypes.guess_type(file_name)[0]

    payload = b""

    if file_name.startswith("/"):
        file_path = Path(file_name)
        if not file_path.is_file():
            status = "404 Not Found"
        else:
            status = "200 OK"
            with file_path.open("rb") as src:
                payload = src.read()
    else:
        try:
            status = "200 OK"
            payload = read_static(file_name)
        except IOError:
            status = "404 Not Found"

    return ResponseT(status, {"Content-Type": content_type}, payload)
