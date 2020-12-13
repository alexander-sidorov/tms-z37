import os
from typing import Optional

from pydantic import BaseModel

from tests.functional.pages.abstract import WebDriverT
from tests.functional.pages.sign_up import SignUpPage
from tests.functional.util.consts import SIGN_UP_URL
from tests.functional.util.consts import URL_LANDING
from tests.functional.util.util import validate_redirect


class Credentials(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None


def sign_up(browser: WebDriverT) -> Credentials:
    current_url = browser.current_url
    credentials = Credentials()

    try:
        page = SignUpPage(browser, SIGN_UP_URL)

        nonce = os.urandom(8).hex()

        page.email = credentials.email = f"test_email_{nonce}@test.com"
        page.password = credentials.password = f"Password_{nonce}_123+"
        page.password_confirmation = credentials.password
        page.username = credentials.username = f"test_user_{nonce}"

        page.sign_up.click()

        validate_redirect(page, URL_LANDING)

    finally:
        browser.get(current_url)

    validate_redirect(page, current_url)

    return credentials
