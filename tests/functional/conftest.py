import pytest

from tests.functional.util.browsers import BrowserFactory


@pytest.yield_fixture(scope="session", autouse=True)
def browser():
    instance = BrowserFactory.get_factory().build()

    yield instance

    instance.close()
    instance.quit()
