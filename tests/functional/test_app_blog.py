import pytest
from delorean import now
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from tests.functional.pages.blog import AllPostsPage
from tests.functional.util.actions.onboarding import sign_in
from tests.functional.util.actions.onboarding import sign_up
from tests.functional.util.consts import URL_BLOG
from tests.functional.util.util import screenshot_on_failure
from tests.functional.util.util import validate_redirect


@pytest.mark.functional
@screenshot_on_failure
def test_anonymous(browser, request):
    page = AllPostsPage(browser, URL_BLOG)
    validate_can_create_posts(page, False)
    validate_number_of_posts(page, 0)


@pytest.mark.functional
@screenshot_on_failure
def test_single_user(browser, request):
    page = AllPostsPage(browser, URL_BLOG)
    validate_number_of_posts(page, 0)

    sign_up(page.browser)

    content = "xxx"

    create_post(page, content)
    validate_number_of_posts(page, 1)

    post = get_post(page, 0)
    validate_post(post, content, True)

    delete_post(page, post)
    validate_number_of_posts(page, 0)

    create_post(page, "yyy")
    create_post(page, "zzz")
    validate_number_of_posts(page, 2)

    wipe_posts(page)
    validate_number_of_posts(page, 0)


@pytest.mark.functional
@screenshot_on_failure
def test_two_users(browser, request):
    page = AllPostsPage(browser, URL_BLOG)
    validate_number_of_posts(page, 0)

    user1 = sign_up(page.browser)
    user2 = sign_up(page.browser)

    sign_in(page.browser, user1)

    create_post(page, user1.username)
    validate_number_of_posts(page, 1)

    sign_in(page.browser, user2)
    validate_number_of_posts(page, 1)
    create_post(page, user2.username)
    validate_number_of_posts(page, 2)

    sign_in(page.browser, user1)
    post = get_post(page, 0)
    validate_can_delete_post(post, False)
    post = get_post(page, 1)
    validate_can_delete_post(post, True)

    sign_in(page.browser, user2)
    post = get_post(page, 0)
    validate_can_delete_post(post, True)
    post = get_post(page, 1)
    validate_can_delete_post(post, False)

    sign_in(page.browser, user1)
    wipe_posts(page)
    validate_number_of_posts(page, 1)
    post = get_post(page, 0)
    validate_can_delete_post(post, False)

    sign_in(page.browser, user2)
    wipe_posts(page)
    validate_number_of_posts(page, 0)


@pytest.mark.functional
@screenshot_on_failure
def test_likes(browser, request):
    page = AllPostsPage(browser, URL_BLOG)
    validate_number_of_posts(page, 0)

    sign_up(page.browser)
    create_post(page, "xxx")
    post = get_post(page, 0)

    validate_number_of_likes(post, 0)
    like(post)
    validate_number_of_likes(post, 0)

    sign_up(page.browser)
    post = get_post(page, 0)
    validate_number_of_likes(post, 0)
    like(post)
    validate_number_of_likes(post, 1)
    like(post)
    validate_number_of_likes(post, 0)

    wipe_posts(page)


def validate_number_of_posts(page: AllPostsPage, number: int) -> None:
    if not number:
        assert not page.posts
    else:
        assert len(page.posts) == number, "invalid posts amount"


def validate_number_of_likes(post: WebElement, expected_number_of_likes: int) -> None:
    likes = post.find_element_by_css_selector("span.likes")
    actual_number_of_likes = int(likes.text)
    assert actual_number_of_likes == expected_number_of_likes


def like(post: WebElement):
    likes = post.find_element_by_css_selector("span.likes")
    likes.click()


def get_post(page: AllPostsPage, number: int) -> WebElement:
    post = page.posts[number]
    return post


def validate_post(post: WebElement, content: str, can_delete=False) -> None:
    validate_post_tag(post)
    validate_post_content(post, content)
    validate_post_date(post)
    validate_post_views(post)
    validate_post_likes(post)
    validate_can_delete_post(post, can_delete)


def validate_post_tag(post: WebElement) -> None:
    assert post.tag_name == "article"


def validate_post_content(post: WebElement, content: str) -> None:
    content_tag = post.find_element_by_css_selector("span.content")
    assert content_tag.text == content


def validate_post_date(post: WebElement) -> None:
    date = post.find_element_by_css_selector("a.date")
    assert str(now().date.year) in date.text.strip()  # oh my...


def validate_post_views(post: WebElement) -> None:
    views = post.find_element_by_css_selector("span.views")
    assert "👁" in views.text


def validate_post_likes(post: WebElement) -> None:
    likes = post.find_element_by_css_selector("span.likes")
    assert likes.text.isdigit()


def validate_can_create_posts(page: AllPostsPage, can: bool) -> None:
    try:
        assert page.content.tag_name == "textarea"
        actually_can = True
    except NoSuchElementException:
        actually_can = False

    assert actually_can == can, f"can{'' if actually_can else ' not'} create posts"


def validate_can_delete_post(post: WebElement, can: bool) -> None:
    try:
        delete = get_delete_button(post)
        assert delete.text == "❌"
        actually_can = True
    except NoSuchElementException:
        actually_can = False

    assert actually_can == can, f"can{'' if actually_can else ' not'} delete post"


def create_post(page: AllPostsPage, content: str) -> None:
    page.content = content
    page.tell.click()
    validate_redirect(page, URL_BLOG)


def delete_post(page: AllPostsPage, post: WebElement) -> None:
    delete = get_delete_button(post)
    delete.click()
    validate_redirect(page, URL_BLOG)


def get_delete_button(post: WebElement) -> WebElement:
    delete = post.find_element_by_css_selector("form.delete button[type=submit]")
    return delete


def wipe_posts(page: AllPostsPage):
    page.wipe.click()
    validate_redirect(page, URL_BLOG)
