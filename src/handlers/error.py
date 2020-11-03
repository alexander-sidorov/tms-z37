from framework.types import RequestT
from framework.types import ResponseT


def handle_error(request: RequestT) -> ResponseT:
    1 / 0
