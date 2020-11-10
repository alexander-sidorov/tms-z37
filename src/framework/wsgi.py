from framework import errors
from framework import types
from framework import utils
from handlers import get_handler_and_kwargs
from handlers import special


def application(environ: dict, start_response):
    path = utils.get_request_path(environ)
    method = utils.get_request_method(environ)
    handler, kwargs = get_handler_and_kwargs(path)
    request_headers = utils.get_request_headers(environ)
    query = utils.get_request_query(environ)
    body = utils.get_request_body(environ)
    form_data = utils.build_form_data(body)

    request = types.RequestT(
        body=body,
        form_data=form_data,
        headers=request_headers,
        kwargs=kwargs,
        method=method,
        path=path,
        query=query,
    )

    try:
        response = handler(request)
    except errors.NotFound:
        response = special.handle_404(request)
    except errors.MethodNotAllowed:
        response = special.handle_405(request)
    except Exception:
        response = special.handle_500(request)

    start_response(response.status, list((response.headers or {}).items()))

    yield response.payload or b""
