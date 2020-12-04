from django.views.generic import CreateView
from django.views.generic import ListView

from applications.blog.models import Post


class AllPostsView(ListView):
    template_name = "blog/index.html"
    model = Post


class NewPostView(CreateView):
    model = Post
    fields = ["content"]
    success_url = "/b/"
