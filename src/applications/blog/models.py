import delorean
from django.db import models


def _now():
    return delorean.utcnow().datetime


class Post(models.Model):
    title = models.TextField(null=True, blank=True, unique=True)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=_now)
    nr_likes = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]
