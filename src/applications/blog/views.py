from django.http import HttpRequest
from django.shortcuts import redirect
from django.shortcuts import render

from applications.blog.models import Post


def all_posts_view(request):
    context = {
        "object_list": Post.objects.all(),
    }

    response = render(request, "blog/index.html", context=context)
    return response


def new_post_view(request: HttpRequest):
    content = request.POST["content"]

    post = Post(
        content=content,
    )
    post.save()

    return redirect("/b/")
