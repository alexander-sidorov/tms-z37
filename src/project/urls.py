from django.contrib import admin
from django.http import HttpRequest
from django.http import HttpResponse
from django.urls import path


def index(_request: HttpRequest) -> HttpResponse:
    return HttpResponse("xxx")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
]
