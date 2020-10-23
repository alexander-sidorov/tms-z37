import random
from mimetypes import guess_type

from framework.consts import DIR_STATIC


def application(environ, start_response):
    url = environ["PATH_INFO"]

    file_names = {"/xxx/": "styles.css", "/logo.png/": "logo.png", "/": "index.html"}

    file_name = file_names.get(url)

    if file_name is not None:
        status = "200 OK"
        headers = {
            "Content-type": guess_type(file_name)[0],
        }
        payload = read_static(file_name)
    else:
        status = "404 Not Found"
        headers = {
            "Content-type": "text/plain",
        }
        payload = generate_404(environ)

    start_response(status, list(headers.items()))

    yield payload


def read_static(file_name: str) -> bytes:
    path = DIR_STATIC / file_name

    with path.open("rb") as fp:
        payload = fp.read()

    return payload


def generate_404(environ) -> bytes:
    url = environ["PATH_INFO"]
    pin = random.randint(1, 1000)

    msg = f"Hello world! Your path: {url} not found. Pin: {pin}"

    return msg.encode()
