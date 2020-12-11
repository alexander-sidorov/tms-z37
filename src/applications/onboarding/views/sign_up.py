from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView

from applications.onboarding.forms import SignUpForm


class SignUpView(FormView):
    form_class = SignUpForm
    success_url = reverse_lazy("landing:index")
    template_name = "onboarding/sign-up.html"

    def form_valid(self, form):
        form.save()

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]

        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)

        return super().form_valid(form)
