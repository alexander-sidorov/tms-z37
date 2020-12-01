from django.http import HttpResponse


def index(*a, **kw):
    return HttpResponse("blog works")
