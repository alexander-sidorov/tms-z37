import io
import json
import os

import pytest

from framework import utils
from framework.types import StaticT


@pytest.mark.unit
def test_http_first():
    normal_header = ("CONTENT_LENGTH", "")
    http_header = ("HTTP_ACCEPT", "")

    ordered_header = utils.http_first(normal_header)
    assert ordered_header == (1, normal_header)

    ordered_header = utils.http_first(http_header)
    assert ordered_header == (0, http_header)


@pytest.mark.unit
def test_format_env_var():
    env_name, env_value = "XXX", "X:Y:Z"
    formatted_value = utils.format_env_var(env_name, env_value)
    assert formatted_value == env_value

    env_name, env_value = "PATH", "X:Y:Z"
    formatted_value = utils.format_env_var(env_name, env_value)
    assert formatted_value == "X<br>Y<br>Z"

    env_name, env_value = "ACCEPT", "X, Y;Z,W"
    formatted_value = utils.format_env_var(env_name, env_value)
    assert formatted_value == "X<br>Y;Z<br>W"


@pytest.mark.unit
def test_read_static(mocker, tmp_path):
    hsh = os.urandom(16).hex()
    static_file_name = f"{hsh}.json"
    static_file = tmp_path / static_file_name
    data = {"x": "y"}

    with static_file.open("w") as dst:
        json.dump(data, dst)

    mocker.patch.object(utils, "DIR_STATIC", tmp_path.resolve())

    static = utils.read_static(static_file_name)
    assert isinstance(static, StaticT)
    assert static.content_type == "application/json"
    assert static.content == json.dumps(data).encode()

    static = utils.read_static(static_file.resolve().as_posix())
    assert isinstance(static, StaticT)
    assert static.content_type == "application/json"
    assert static.content == json.dumps(data).encode()


@pytest.mark.unit
def test_get_request_headers():
    environ = {
        "CONTENT_LENGTH": "1",
        "HTTP_ACCEPT": "xxx",
    }

    headers = utils.get_request_headers(environ)

    assert headers == {"ACCEPT": environ["HTTP_ACCEPT"]}


@pytest.mark.unit
def test_get_request_query():
    query = utils.get_request_query({})
    assert query == {}

    query = utils.get_request_query({"QUERY_STRING": "x=1&x=2&y=3"})
    assert query == {"x": ["1", "2"], "y": ["3"]}


@pytest.mark.unit
def test_build_status():
    status = utils.build_status(200)
    assert status == "200 OK"

    status = utils.build_status(400)
    assert status == "400 Bad Request"

    status = utils.build_status(404)
    assert status == "404 Not Found"

    status = utils.build_status(500)
    assert status == "500 Internal Server Error"


@pytest.mark.unit
def test_build_form_data():
    body = b"x=1&x=2&y=3"
    form_data = utils.build_form_data(body)
    assert form_data == {"x": ["1", "2"], "y": ["3"]}


@pytest.mark.unit
def test_get_request_body():
    environ = {}
    body = utils.get_request_body(environ)
    assert body is None

    environ = {"wsgi.input": 1}
    body = utils.get_request_body(environ)
    assert body is None

    environ = {"wsgi.input": 1, "REQUEST_METHOD": "POST"}
    body = utils.get_request_body(environ)
    assert body is None

    environ = {"wsgi.input": 1, "CONTENT_LENGTH": "123"}
    body = utils.get_request_body(environ)
    assert body is None

    src = io.BytesIO()
    content = b"xxx"
    src.write(content)
    src.seek(0)
    environ = {
        "wsgi.input": src,
        "REQUEST_METHOD": "POST",
        "CONTENT_LENGTH": str(len(content)),
    }
    body = utils.get_request_body(environ)
    assert body == content
