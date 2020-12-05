from django.urls import path

from applications.landing.views import IndexView

urlpatterns = [
    path("", IndexView.as_view()),
]
