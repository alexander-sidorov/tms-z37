from selenium.webdriver.common.by import By

from .abstract import PageElement
from .abstract import PageObject


class SignUpPage(PageObject):
    username = PageElement(By.CSS_SELECTOR, "#id_sign_up_form #id_username")
    email = PageElement(By.CSS_SELECTOR, "#id_sign_up_form #id_email")
    password = PageElement(By.CSS_SELECTOR, "#id_sign_up_form #id_password1")
    password_confirmation = PageElement(
        By.CSS_SELECTOR, "#id_sign_up_form #id_password2"
    )
    sign_up = PageElement(By.CSS_SELECTOR, "#id_sign_up_form #id_sign_up_submit")
    next = PageElement(By.CSS_SELECTOR, "#id_sign_up_form #id_sign_up_next")
