from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("", include("applications.landing.urls")),
    path("admin/", admin.site.urls),
    path("b/", include("applications.blog.urls")),
    path("e/", lambda _r: 1 / 0, name="error"),
    path("h/", include("applications.hello.urls")),
    path("o/", include("applications.onboarding.urls")),
]
