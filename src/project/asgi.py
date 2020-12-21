import os

from django.core.asgi import get_asgi_application

from api.main import app

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")


async def application(scope, receive, send):
    path = scope["path"]

    if path.startswith("/api"):
        _app = app
    else:
        _app = get_asgi_application()

    return await _app(scope, receive, send)
