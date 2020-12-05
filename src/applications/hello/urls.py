from django.urls import path

from applications.hello import views

urlpatterns = {
    path("", views.HelloView.as_view()),
    path("reset/", views.HelloResetView.as_view()),
}
