from django.urls import path

from applications.blog import views

urlpatterns = [
    path("", views.AllPostsView.as_view()),
    path("new/", views.NewPostView.as_view()),
    path("wipe/", views.WipeView.as_view()),
]
