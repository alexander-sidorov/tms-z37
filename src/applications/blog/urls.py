from django.urls import path

from applications.blog import views
from applications.blog.apps import BlogConfig

app_name = BlogConfig.label

urlpatterns = [
    path("", views.AllPostsView.as_view(), name="all"),
    path("new/", views.NewPostView.as_view(), name="new"),
    path("wipe/", views.WipeView.as_view(), name="wipe"),
    path("post/<int:pk>/", views.SinglePostView.as_view(), name="post"),
    path("post/<int:pk>/update/", views.UpdatePostView.as_view(), name="update"),
    path("post/<int:pk>/delete/", views.DeletePostView.as_view(), name="delete"),
]
