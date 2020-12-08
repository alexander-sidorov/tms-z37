from django.urls import path

from applications.blog import views
from applications.blog.apps import BlogConfig

app_name = BlogConfig.label

urlpatterns = [
    path("", views.AllPostsView.as_view(), name="all"),
    path("new/", views.NewPostView.as_view(), name="new"),
    path("wipe/", views.WipeAllPostsView.as_view(), name="wipe"),
    path("post/<int:pk>/", views.PostView.as_view(), name="post"),
    path("post/<int:pk>/delete/", views.DeletePostView.as_view(), name="delete"),
]
