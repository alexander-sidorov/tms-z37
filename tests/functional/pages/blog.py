from selenium.webdriver.common.by import By

from .abstract import PageElement
from .abstract import PageElements
from .abstract import PageObject


class AllPostsPage(PageObject):
    posts = PageElements(By.CSS_SELECTOR, "article")
    content = PageElement(By.CSS_SELECTOR, "textarea#id_content")
    tell = PageElement(By.CSS_SELECTOR, "#id_post_form_submit")
    wipe = PageElement(By.CSS_SELECTOR, "#id_post_form_wipe")
