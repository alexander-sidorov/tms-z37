from django.shortcuts import render

from applications.blog.models import Post


def index(request):
    context = {
        "object_list": Post.objects.all(),
    }

    response = render(request, "blog/index.html", context=context)
    return response
