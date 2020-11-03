import sys
import traceback

from framework.types import RequestT
from framework.types import ResponseT
from framework.utils import read_static


def handle_500(_request: RequestT = None) -> ResponseT:
    error_class, error, tb = sys.exc_info()

    filenames = "".join(
        f"""<li><a href="http://localhost:8000/s{frame.f_code.co_filename}">{frame.f_code.co_filename}</a></li>"""
        for frame, _lineno in traceback.walk_tb(tb)
    )

    document = f"""
        <h1>WASTED</h1>
        <ul>
        {filenames}
        </ul>
    """

    base_html = read_static("_base.html", str)

    document = base_html.format(xxx=document)

    payload = document.encode()
    status = "500 Internal Server Error"
    headers = {"Content-type": "text/html"}

    return ResponseT(status, headers, payload)
