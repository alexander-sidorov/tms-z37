from typing import Dict

from django import forms
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
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
    template_name = "blog/all.html"
    model = Post

    def get_extended_context(self) -> Dict:
        context = {"form": PostForm()}

        return context


class NewPostView(CreateView):
    fields = ["content"]
    http_method_names = ["post"]
    model = Post
    success_url = reverse_lazy("blog:all")


class WipeAllPostsView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        Post.objects.all().delete()
        return reverse_lazy("blog:all")


class PostView(UpdateView):
    fields = ["content"]
    model = Post
    template_name = "blog/post.html"

    def form_valid(self, form):
        self.object.edited = True
        return super().form_valid(form)


class DeletePostView(DeleteView):
    http_method_names = ["post"]
    model = Post
    success_url = reverse_lazy("blog:all")
