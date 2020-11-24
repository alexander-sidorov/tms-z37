from django.urls import path

from applications.landing.views import index

urlpatterns = [
    path("", index),
]
