import sys
import traceback

from framework.types import RequestT
from framework.types import ResponseT
from framework.utils import build_absolute_url
from framework.utils import build_status
from framework.utils import read_static


def handle_500(_request: RequestT = None) -> ResponseT:
    traceback.print_exc()

    error_class, error, tb = sys.exc_info()

    filenames = "".join(
        f"""<p>File <a href="{build_absolute_url("/s/{fn}", fn=frame.f_code.co_filename)}">{frame.f_code.co_filename}</a>, line {lineno}</p>"""
        for frame, lineno in traceback.walk_tb(tb)
    )

    document = f"""
        <h1>WASTED</h1>
        <hr>
        <div class="code">
        {filenames}
        <p>
        {error_class.__name__}: {error}
        </p>
        </div>
    """

    base_html = read_static("_base.html").content.decode()

    document = base_html.format(body=document)

    payload = document.encode()
    status = build_status(500)
    headers = {"Content-type": "text/html"}

    return ResponseT(status, headers, payload)
