import pytest

from tests.functional.pages.hello import HelloPage
from tests.functional.util.util import screenshot_on_failure
from tests.functional.util.util import validate_redirect

url = "http://localhost:8000/h/"


@pytest.mark.functional
@screenshot_on_failure
def test(browser, request):
    page = HelloPage(browser, url)

    assert page.greeting.text == "Hello anonymous"
    assert page.address.text == "You are in nowhere"

    page.name_input.clear()
    page.address_input.clear()
    page.name_input.send_keys("Alex")
    page.submit_button.click()
    validate_redirect(page, url)
    assert page.greeting.text == "Hello Alex"
    assert page.address.text == "You are in nowhere"
    assert page.name_input.get_attribute("value") == "Alex"

    page.name_input.clear()
    page.address_input.clear()
    page.address_input.send_keys("localhost")
    page.submit_button.click()
    validate_redirect(page, url)
    assert page.greeting.text == "Hello anonymous"
    assert page.address.text == "You are in localhost"
    assert page.address_input.get_attribute("value") == "localhost"

    page.name_input.clear()
    page.address_input.clear()
    page.name_input.send_keys("Alex")
    page.address_input.send_keys("localhost")
    page.submit_button.click()
    validate_redirect(page, url)
    assert page.greeting.text == "Hello Alex"
    assert page.address.text == "You are in localhost"
    assert page.name_input.get_attribute("value") == "Alex"
    assert page.address_input.get_attribute("value") == "localhost"
