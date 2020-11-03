from framework.errors import NotFound
from framework.types import RequestT
from framework.utils import get_query
from framework.utils import get_request_headers
from handlers import get_handler_and_kwargs
from handlers import special


def application(environ: dict, start_response):
    path = environ["PATH_INFO"]
    method = environ["REQUEST_METHOD"]
    handler, kwargs = get_handler_and_kwargs(path)
    request_headers = get_request_headers(environ)
    query = get_query(environ)

    request = RequestT(
        headers=request_headers,
        kwargs=kwargs,
        method=method,
        path=path,
        query=query,
    )

    try:
        response = handler(request)
    except NotFound:
        response = special.handle_404(request)
    except Exception:
        response = special.handle_500(request)

    start_response(response.status, list(response.headers.items()))

    yield response.payload
