from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render


def view_hello(request: HttpRequest) -> HttpResponse:
    action_views = {
        "greet": _view_hello_greet,
        "reset": _view_hello_reset,
    }

    action_view = action_views.get("XXX", _view_hello_index)
    if not action_view:
        raise Http404

    response = action_view(request)
    return response


def _view_hello_index(request: HttpRequest) -> HttpResponse:
    response = render(request, "hello/index.html")
    return response


def _view_hello_greet(request: HttpRequest) -> HttpResponse:
    return HttpResponse("xxx")


def _view_hello_reset(request: HttpRequest) -> HttpResponse:
    return HttpResponse("xxx")
