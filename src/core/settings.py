import os
from datetime import timedelta
from os.path import abspath, dirname, exists, join
from typing import Any, Dict

import environ

# Load operating system env variables and prepare to use them
env = environ.Env()

# .env file, should load only in development environment
env_file = join(dirname(__file__), "local.env")
if exists(env_file):
    environ.Env.read_env(str(env_file))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = dirname(dirname(abspath(__file__)))

# Quick-start development settings - unsuitable for production
SECRET_KEY = env(
    "DJANGO_SECRET_KEY", default="8#ubdv*jh_1u(6m4)^s^*pdo!&y_#jz)vv%5cp%8^*&%ztttxq"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", False)
ENVIRONMENT = env("ENV")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])

# AWS
AWS_ACCESS_KEY = env.str("AWS_ACCESS_KEY", default="")
AWS_SECRET_KEY = env.str("AWS_SECRET_KEY", default="")
AWS_REGION = env.str("AWS_REGION", default="")

# CORS
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=False)
if not CORS_ALLOW_ALL_ORIGINS:
    CORS_ALLOWED_ORIGINS = env.str(
        "CORS_ALLOWED_ORIGINS", default="localhost,127.0.0.1"
    ).split(",")

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "drf_spectacular",
    "django_extensions",
    "rest_framework_simplejwt.token_blacklist",
]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

PROJECT_APPS = ["core", "authentication", "transactions"]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "authentication.middleware.token_middleware.TokenMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "core.wsgi.application"

# Django debug toolbar settings

if ENVIRONMENT == "development":
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INTERNAL_IPS = env.list("INTERNAL_IPS", default=[])
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: request.headers.get("x-requested-with")
        != "XMLHttpRequest"
    }

# Database

DATABASES = {"default": env.db()}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"}
]

# Internationalization

LANGUAGE_CODE = "en-us"
LANGUAGES = [
    ("en-us", "English"),
]
USE_I18N = True
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)


TIME_ZONE = "UTC"

USE_I18N = True


USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS: list[str] = []

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

SITE_ID = 1

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files (uploads)

if ENVIRONMENT in ("development", "testing"):
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    MEDIA_ROOT = "uploads/"
    MEDIA_URL = "/uploads/"

# Email settings

if ENVIRONMENT in ("development", "testing"):
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "no-reply@localhost"

# Django Rest Framework Settings

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "authentication.utils.jwt.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Auth

AUTH_USER_MODEL = "core.User"
FORGOT_TIME_EXPIRATION_TIME = timedelta(days=1)

# Sentry
SENTRY_DSN = env.str("SENTRY_DSN", default=None)
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENVIRONMENT,
        integrations=[DjangoIntegration()],
    )

SPECTACULAR_SETTINGS = {
    "TITLE": "python-django",
    "VERSION": "1.0.0",
    "DESCRIPTION": "API Documentation",
}

# Logging
LOGGING: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "main_formatter": {
            "format": "%(levelname)s:%(name)s: %(message)s "
            "(%(asctime)s; %(filename)s:%(lineno)d)",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "main_formatter",
        },
    },
    "loggers": {
        "root": {
            "level": "INFO",
            "handlers": ["console"],
        },
    },
}

# CloudWatch Logging settings
AWS_CLOUDWATCH_LOG_GROUP_NAME = env.str("AWS_CLOUDWATCH_LOG_GROUP_NAME", default="")
if AWS_CLOUDWATCH_LOG_GROUP_NAME:
    import boto3

    boto3_logs_client = boto3.client(
        "logs",
        region_name=AWS_REGION,
    )
    LOGGING["handlers"]["cloudwatch"] = {
        "boto3_client": boto3_logs_client,
        "class": "logging.handlers.CloudWatchLogHandler",
        "level": "INFO",
        "filters": ["require_debug_false"],
        "formatter": "main_formatter",
        "log_group": AWS_CLOUDWATCH_LOG_GROUP_NAME,
        "stream_name": "cloudwatch",
    }
    LOGGING["loggers"]["root"]["handlers"].append("cloudwatch")

# SimpleJWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=int(env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=5))
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=int(env.int("REFRESH_TOKEN_EXPIRE_DAYS", default=5))
    ),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "SIGNING_KEY": env.str("JWT_SECRET_KEY", default=SECRET_KEY),
    "AUTH_HEADER_TYPES": ("Bearer", "Token"),
}
