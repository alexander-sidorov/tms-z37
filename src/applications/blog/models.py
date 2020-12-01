from django.db import models


class Post(models.Model):
    title = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField()
    nr_likes = models.IntegerField()
