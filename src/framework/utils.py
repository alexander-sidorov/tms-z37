import re
from html import escape
from typing import Any
from typing import Callable
from typing import Dict
from typing import Tuple

from framework.consts import DIR_STATIC


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


def read_static(file_name: str, converter: Callable = bytes) -> Any:
    path = DIR_STATIC / file_name

    modes: Dict[Any, str] = {
        str: "r",
    }

    mode = modes.get(converter, "rb")

    with path.open(mode) as fp:
        payload = fp.read()

    return converter(payload)
