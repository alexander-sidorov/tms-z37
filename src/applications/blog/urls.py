from django.urls import path

from applications.blog.views import index

urlpatterns = [
    path("", index),
]
