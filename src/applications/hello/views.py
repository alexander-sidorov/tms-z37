from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render


def view_hello_index(request: HttpRequest) -> HttpResponse:
    response = render(request, "hello/index.html")
    return response


def view_hello_greet(request: HttpRequest) -> HttpResponse:
    return HttpResponse("xxx")


def view_hello_reset(request: HttpRequest) -> HttpResponse:
    return HttpResponse("xxx")
