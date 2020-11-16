class HttpError(RuntimeError):
    pass


class NotFound(HttpError):
    pass


class MethodNotAllowed(HttpError):
    pass
