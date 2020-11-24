from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render


def view_hello_index(request: HttpRequest) -> HttpResponse:
    name = request.session.get("name")
    address = request.session.get("address")

    context = {
        "address_header": address or "nowhere",
        "address_value": address or "",
        "name_header": name or "anonymous",
        "name_value": name or "",
    }
    response = render(request, "hello/index.html", context=context)
    return response


def view_hello_greet(request: HttpRequest) -> HttpResponse:
    name = request.POST.get("name")
    address = request.POST.get("address")

    request.session["name"] = name
    request.session["address"] = address

    return redirect("/h/")


def view_hello_reset(request: HttpRequest) -> HttpResponse:
    request.session.clear()
    return redirect("/h/")
