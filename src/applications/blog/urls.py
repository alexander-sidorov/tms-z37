from django.urls import path

from applications.blog import views

urlpatterns = [
    path("", views.index),
    path("new/", views.new_post_view),
]
