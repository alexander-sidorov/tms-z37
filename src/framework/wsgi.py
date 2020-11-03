from framework.types import RequestT
from handlers import handle_index
from handlers import handle_logo
from handlers import handle_styles
from handlers import make_error
from handlers import special

handlers = {
    "/": handle_index,
    "/logo.png/": handle_logo,
    "/xxx/": handle_styles,
    "/e/": make_error,
}


def application(environ: dict, start_response):
    try:
        path = environ["PATH_INFO"]

        handler = handlers.get(path, special.handle_404)

        request_headers = {
            key[5:]: environ[key]
            for key in filter(lambda i: i.startswith("HTTP_"), environ)
        }

        request = RequestT(
            method=environ["REQUEST_METHOD"],
            path=path,
            headers=request_headers,
        )

        response = handler(request)
    except Exception:
        response = special.handle_500()

    start_response(response.status, list(response.headers.items()))

    yield response.payload
