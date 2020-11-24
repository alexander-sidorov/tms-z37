from django.urls import path

from applications.hello import views

urlpatterns = [
    path("", views.view_hello_index),
    path("greet/", views.view_hello_greet),
    path("reset/", views.view_hello_reset),
]
