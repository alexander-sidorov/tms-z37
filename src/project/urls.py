from django.contrib import admin
from django.http import HttpRequest
from django.http import HttpResponse
from django.urls import path

from framework.utils import read_static


def index(_request: HttpRequest) -> HttpResponse:
    base = read_static("_base.html")
    base_html = base.content.decode()
    index_html = read_static("index.html").content.decode()

    result = base_html.format(body=index_html)
    result = result.encode()

    return HttpResponse(result)


urlpatterns = [
    path("", index),
    path("admin/", admin.site.urls),
]
