from django.urls import path

from applications.hello import views
from applications.hello.apps import HelloConfig

app_name = HelloConfig.label

urlpatterns = [
    path("", views.HelloView.as_view(), name="greet"),
    path("reset/", views.HelloResetView.as_view(), name="reset"),
]
