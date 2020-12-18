import delorean
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Manager
from django.urls import reverse_lazy

User = get_user_model()


def _now():
    return delorean.utcnow().datetime


class PostManager(Manager):
    pass


class Post(models.Model):
    objects = PostManager()

    content = models.TextField(null=True, blank=True)

    nr_views = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=_now)
    edited = models.BooleanField(default=False)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likers = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    @property
    def nr_likes(self):
        return self.likers.count()

    def is_liked_by(self, user: User) -> bool:
        liked = Post.objects.filter(pk=self.pk, likers=user).exists()
        return liked

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        kwargs = {"pk": self.pk}
        url = reverse_lazy("blog:post", kwargs=kwargs)
        return url
