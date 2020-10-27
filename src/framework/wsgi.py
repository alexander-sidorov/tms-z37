import random
import re
from html import escape
from mimetypes import guess_type
from typing import Any
from typing import Callable
from typing import Tuple

from framework.consts import DIR_STATIC


def application(environ, start_response):
    url = environ["PATH_INFO"]

    file_names = {
        "/xxx/": "styles.css",
        "/logo.png/": "logo.png",
        "/": "index.html",
    }

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
            "Content-type": "text/html",
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
    pin = random.randint(1, 999999)

    environ_pairs = "\n".join(
        f"<div class=\"pair {'http' if env_var_name.startswith('HTTP') else ''}\">"
        f"<p>{escape(str(env_var_name))}</p>"
        f"<p>{format_env_var(env_var_name, env_var_value)}</p>"
        f"</div>"
        for env_var_name, env_var_value in sorted(environ.items(), key=http_first)
    )

    msg = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <title>Z37 :: Not found</title>
          <meta charset="utf-8">
          <link href="/xxx/" rel="stylesheet"/>
          <link href="/logo.png/" rel="shortcut icon" type="image/png"/>
        </head>
        <body>
        <h1>OOPS!</h1>
        <hr>
        <h2>The path you've looking for does not exist on this server.</h2>
        <p class="url"><span>{url}</span></p>
        <p>Pin: <span class="pin">{pin:>06}</span></p>
        <div class="environ-table">
        {environ_pairs}
        <div>
        </body>
        </html>
    """

    return msg.encode()


def http_first(value: Tuple[str, Any]) -> tuple:
    if value[0].startswith("HTTP"):
        return 0, value
    return 1, value


def format_env_var(name: str, value: str) -> str:
    formatter = get_formatter(name)
    new = str(value)
    new = formatter(new)
    new = escape(new)
    new = re.sub("\n", "<br>", new)

    return new


def get_formatter(env_var_name: str) -> Callable[[str], str]:
    if env_var_name.endswith("PATH"):
        return lambda _value: "\n".join(_value.split(":"))
    if "ACCEPT" in env_var_name:
        return lambda _v: "\n".join(re.split(r"[\s,]+", _v))
    return lambda _v: _v
