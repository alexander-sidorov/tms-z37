import random
from html import escape

from framework.types import RequestT
from framework.types import ResponseT
from framework.utils import build_status
from framework.utils import format_env_var
from framework.utils import http_first
from framework.utils import read_static


def handle_404(request: RequestT) -> ResponseT:
    url = request.path
    pin = random.randint(1, 999999)

    environ_pairs = "\n".join(
        f"<div class=\"pair {'http' if env_var_name.startswith('HTTP') else ''}\">"
        f"<p>{escape(str(env_var_name))}</p>"
        f"<p>{format_env_var(env_var_name, env_var_value)}</p>"
        f"</div>"
        for env_var_name, env_var_value in sorted(
            request.headers.items(), key=http_first
        )
    )

    base_html = read_static("_base.html").content.decode()

    html_404 = f"""
    <h1>OOPS!</h1>
        <hr>
        <h2>The path you've looking for does not exist on this server.</h2>
        <p class="url"><span>{url}</span></p>
        <p>Pin: <span class="pin">{pin:>06}</span></p>
        <div class="environ-table">
        {environ_pairs}
        <div>
    """

    document = base_html.format(body=html_404)

    payload = document.encode()
    status = build_status(404)
    headers = {"Content-type": "text/html"}

    return ResponseT(status, headers, payload)


def handle_405(request: RequestT) -> ResponseT:
    status = build_status(405)
    payload = f"Resource {request.path} does not support {request.method} requests."
    headers = {"Content-type": "text/plain"}

    return ResponseT(
        status=status,
        headers=headers,
        payload=payload.encode(),
    )
