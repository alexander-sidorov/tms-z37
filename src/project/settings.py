import os
from pathlib import Path

import dj_database_url
import sentry_sdk
from dynaconf import settings as dyn

DEBUG = dyn.MODE_DEBUG

if not DEBUG:
    sentry_sdk.init(dyn.SENTRY_DSN, traces_sample_rate=1.0)

_this_file = Path(__file__).resolve()

DIR_PROJECT = _this_file.parent.resolve()

DIR_SRC = DIR_PROJECT.parent.resolve()

DIR_REPO = DIR_SRC.parent.resolve()

SECRET_KEY = dyn.SECRET_KEY

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    dyn.HOST,
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # ---------------------------
    "applications.hello.apps.HelloConfig",
    "applications.landing.apps.LandingConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [DIR_PROJECT / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

DATABASE_URL = os.getenv("DATABASE_URL", dyn.DATABASE_URL)

DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/s/"

STATIC_ROOT = DIR_REPO / ".static"

STATICFILES_DIRS = [
    DIR_PROJECT / "static",
]

if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
