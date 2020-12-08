from typing import Dict

from django import forms
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from applications.blog.models import Post
from framework.mixins import ExtendedContextMixin


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        widgets = {"content": forms.Textarea(attrs={"rows": 2})}


class AllPostsView(ExtendedContextMixin, ListView):
    template_name = "blog/index.html"
    model = Post

    def get_extended_context(self) -> Dict:
        context = {"form": PostForm()}

        return context


class NewPostView(CreateView):
    http_method_names = ["post"]
    model = Post
    fields = ["content"]
    success_url = "/b/"


class WipeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        Post.objects.all().delete()
        return "/b/"


class SinglePostView(DetailView):
    template_name = "blog/post.html"
    model = Post


class UpdatePostView(UpdateView):
    pass


class DeletePostView(DeleteView):
    http_method_names = ["post"]
    model = Post
    success_url = reverse("all")
