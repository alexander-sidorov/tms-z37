from handlers import handle_index
from handlers import handle_logo
from handlers import handle_styles
from handlers import system_handlers

handlers = {
    "/": handle_index,
    "/logo.png/": handle_logo,
    "/xxx/": handle_styles,
}


def application(environ, start_response):
    url = environ["PATH_INFO"]

    handler = handlers.get(url, system_handlers.handle_404)

    status, headers, payload = handler(environ)

    start_response(status, list(headers.items()))

    yield payload
