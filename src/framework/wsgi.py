import re

from framework.types import RequestT
from handlers import handle_index
from handlers import handle_logo
from handlers import handle_styles
from handlers import make_error
from handlers import special

handlers = {
    r"^/logo.png/$": handle_logo,
    r"^/xxx/$": handle_styles,
    r"^/e/$": make_error,
    r"^/s/(?P<file_name>.+)$": special.handle_static,
    r"^/$": handle_index,
}


def application(environ: dict, start_response):
    try:
        path = environ["PATH_INFO"]

        handler = special.handle_404
        kwargs = {}

        for path_pattern, handler in handlers.items():
            if m := re.match(path_pattern, path):
                kwargs = m.groupdict()
                break

        request_headers = {
            key[5:]: environ[key]
            for key in filter(lambda i: i.startswith("HTTP_"), environ)
        }

        request = RequestT(
            headers=request_headers,
            kwargs=kwargs,
            method=environ["REQUEST_METHOD"],
            path=path,
        )

        response = handler(request)
    except Exception:
        response = special.handle_500()

    start_response(response.status, list(response.headers.items()))

    yield response.payload
