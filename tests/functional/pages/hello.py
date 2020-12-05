from selenium.webdriver.common.by import By

from .abstract import PageElement
from .abstract import PageObject


class HelloPage(PageObject):
    greeting = PageElement(By.CSS_SELECTOR, "#greeting_display_id")
    address = PageElement(By.CSS_SELECTOR, "#address_display_id")
    name_input = PageElement(By.CSS_SELECTOR, "#id_name")
    address_input = PageElement(By.CSS_SELECTOR, "#id_address")
    submit_button = PageElement(By.CSS_SELECTOR, "#submit_id")
