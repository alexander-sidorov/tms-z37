from django.contrib.auth.views import LoginView


class SignInView(LoginView):
    template_name = "onboarding/sign-in.html"
