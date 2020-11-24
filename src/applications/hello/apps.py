from django.apps import AppConfig


class HelloConfig(AppConfig):
    label = "hello"
    name = f"applications.{label}"
