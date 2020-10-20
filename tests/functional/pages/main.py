from selenium.webdriver.common.by import By

from .abstract import PageElement
from .abstract import PageObject


class MainPage(PageObject):
    h1 = PageElement(By.XPATH, "/html/body/h1[1]")
    h12 = PageElement(By.XPATH, "/html/body/h1[2]")
    p = PageElement(By.CSS_SELECTOR, "p")
    logo = PageElement(By.CSS_SELECTOR, "img")
