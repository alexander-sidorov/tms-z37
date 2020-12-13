from selenium.webdriver.common.by import By

from .abstract import PageElement
from .abstract import PageObject


class SignInPage(PageObject):
    username = PageElement(By.CSS_SELECTOR, "#id_sign_in_form #id_username")
    password = PageElement(By.CSS_SELECTOR, "#id_sign_in_form #id_password")
    sign_in = PageElement(By.CSS_SELECTOR, "#id_sign_in_form  #id_sign_in_submit")
    next = PageElement(By.CSS_SELECTOR, "#id_sign_in_form #id_sign_in_next")
