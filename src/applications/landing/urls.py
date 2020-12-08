from django.urls import path

from applications.landing import views
from applications.landing.apps import LandingConfig

app_name = LandingConfig.label

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
]
