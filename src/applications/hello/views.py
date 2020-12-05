from typing import Dict

from django import forms
from django.views.generic import FormView
from django.views.generic import RedirectView

from framework.mixins import ExtendedContextMixin


class HelloForm(forms.Form):
    name = forms.CharField(required=False)
    address = forms.CharField(required=False)


class HelloView(ExtendedContextMixin, FormView):
    form_class = HelloForm
    success_url = "/h/"
    template_name = "hello/index.html"

    def get_initial(self):
        return self.get_extended_context()

    def get_extended_context(self) -> Dict:
        name = self.request.session.get("name")
        address = self.request.session.get("address")

        context = {
            "address": address,
            "name": name,
        }

        return context

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        address = form.cleaned_data["address"]
        self.request.session["name"] = name
        self.request.session["address"] = address
        return super().form_valid(form)


class HelloResetView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        self.request.session.clear()
        return "/h/"
