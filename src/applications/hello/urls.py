from django.urls import path

from applications.hello.views import view_hello

urlpatterns = [
    path("", view_hello),
]
