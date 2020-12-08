from django.urls import path

from applications.blog import views

# app_name = "blog"

urlpatterns = [
    path("", views.AllPostsView.as_view(), name="all"),
    path("new/", views.NewPostView.as_view()),
    path("wipe/", views.WipeView.as_view()),
    path("post/<int:pk>/", views.SinglePostView.as_view()),
    # path("post/<int:pk>/update/", views.UpdatePostView.as_view()),
    path("post/<int:pk>/delete/", views.DeletePostView.as_view()),
]
