import delorean
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy

User = get_user_model()


def _now():
    return delorean.utcnow().datetime


class Post(models.Model):
    content = models.TextField(null=True, blank=True)
    nr_likes = models.IntegerField(default=0)

    nr_views = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=_now)
    edited = models.BooleanField(default=False)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        kwargs = {"pk": self.pk}
        url = reverse_lazy("blog:post", kwargs=kwargs)
        return url
