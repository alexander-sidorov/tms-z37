from handlers.index import handle_index
from handlers.logo import handle_logo
from handlers.not_found import handle_404
from handlers.styles import handle_styles

handlers = {
    "/": handle_index,
    "/logo.png/": handle_logo,
    "/xxx/": handle_styles,
}


def application(environ, start_response):
    url = environ["PATH_INFO"]

    handler = handlers.get(url, handle_404)

    status, headers, payload = handler(environ)

    start_response(status, list(headers.items()))

    yield payload
