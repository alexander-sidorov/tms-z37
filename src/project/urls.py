from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("", include("applications.landing.urls")),
    path("admin/", admin.site.urls),
    path("h/", include("applications.hello.urls")),
]
