import delorean
from django.db import models


def _now():
    return delorean.utcnow().datetime


class Post(models.Model):
    content = models.TextField(null=True, blank=True)
    nr_likes = models.IntegerField(default=0)

    nr_views = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=_now)
    edited = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
