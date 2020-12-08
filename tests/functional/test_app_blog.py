import pytest
from delorean import now

from tests.functional.pages.blog import AllPostsPage
from tests.functional.util.util import screenshot_on_failure
from tests.functional.util.util import validate_redirect

url = "http://localhost:8000/b/"


@pytest.mark.functional
@screenshot_on_failure
def test_all_posts(browser, request):
    page = AllPostsPage(browser, url)

    assert not page.content.text
    assert not page.posts
    assert page.tell.text == "Tell"
    assert page.wipe.text == "Wipe"


@pytest.mark.functional
@screenshot_on_failure
def test_create_post(browser, request):
    page = AllPostsPage(browser, url)

    try:
        assert not page.posts

        page.content.send_keys("xxx")
        page.tell.click()
        validate_redirect(page, url)

        posts = list(page.posts)
        assert len(posts) == 1

        post = posts[0]
        assert post.tag_name == "article"

        content = post.find_element_by_css_selector("span.content")
        assert content.text == "xxx"

        delete = post.find_element_by_css_selector("form.delete button[type=submit]")
        assert delete.text == "❌"

        date = post.find_element_by_css_selector("a.date")
        assert str(now().date.year) in date.text.strip()  # oh my...

        views = post.find_element_by_css_selector("span.views")
        assert "👁" in views.text

        likes = post.find_element_by_css_selector("span.likes")
        assert likes.text.isdigit()

        delete.click()
        validate_redirect(page, url)

        posts = list(page.posts)
        assert len(posts) == 0

        page.content.send_keys("yyy")
        page.tell.click()
        validate_redirect(page, url)

        page.wipe.click()
        validate_redirect(page, url)
        posts = list(page.posts)
        assert len(posts) == 0

    finally:
        page.wipe.click()
