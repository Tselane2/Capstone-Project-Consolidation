import os
import sys
from pathlib import Path
from decouple import config, Csv

# Detect when Sphinx is running
IS_SPHINX = "sphinx" in sys.modules

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Environment‑dependent settings
# ---------------------------------------------------------------------------
if IS_SPHINX:
    # Dummy values so Sphinx can import Django without crashing
    SECRET_KEY = "dummy-secret-key"
    DEBUG = True
    ALLOWED_HOSTS = ["*"]
    CSRF_TRUSTED_ORIGINS = []
else:
    SECRET_KEY = config("SECRET_KEY", default="django-insecure-change-me-in-production")
    DEBUG = config("DEBUG", default=True, cast=bool)
    ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*", cast=Csv())

    _replit_domain = os.environ.get("REPLIT_DEV_DOMAIN", "")
    if _replit_domain:
        _default_trusted = f"https://{_replit_domain},https://{_replit_domain}:8000"
    else:
        _default_trusted = ""

    CSRF_TRUSTED_ORIGINS = config(
        "CSRF_TRUSTED_ORIGINS",
        default=_default_trusted,
        cast=Csv(),
    )

# ---------------------------------------------------------------------------
# Installed apps
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "newsapp",
]

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "news_project.urls"

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "news_project.wsgi.application"

# ---------------------------------------------------------------------------
# Database — MariaDB/MySQL (default)
# ---------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config("DB_NAME", default="news_app"),
        'USER': config("DB_USER", default="root"),
        'PASSWORD': config("DB_PASSWORD", default="yourpassword"),
        'HOST': config("DB_HOST", default="localhost"),
        'PORT': config("DB_PORT", default="3306"),
    }
}

# ---------------------------------------------------------------------------
# Optional: SQLite (for quick local testing)
# ---------------------------------------------------------------------------
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# ---------------------------------------------------------------------------
# Custom user model
# ---------------------------------------------------------------------------
AUTH_USER_MODEL = "newsapp.User"

# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static files
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Django REST Framework
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

# ---------------------------------------------------------------------------
# Email settings
# ---------------------------------------------------------------------------
if IS_SPHINX:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 25
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
    EMAIL_USE_TLS = False
    DEFAULT_FROM_EMAIL = "noreply@example.com"
else:
    EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
    EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
    EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
    EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
    DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@newsapp.com")

# ---------------------------------------------------------------------------
# Twitter / X API
# ---------------------------------------------------------------------------
if IS_SPHINX:
    TWITTER_BEARER_TOKEN = ""
    TWITTER_API_KEY = ""
    TWITTER_API_SECRET = ""
    TWITTER_ACCESS_TOKEN = ""
    TWITTER_ACCESS_TOKEN_SECRET = ""
else:
    TWITTER_BEARER_TOKEN = config("TWITTER_BEARER_TOKEN", default="")
    TWITTER_API_KEY = config("TWITTER_API_KEY", default="")
    TWITTER_API_SECRET = config("TWITTER_API_SECRET", default="")
    TWITTER_ACCESS_TOKEN = config("TWITTER_ACCESS_TOKEN", default="")
    TWITTER_ACCESS_TOKEN_SECRET = config("TWITTER_ACCESS_TOKEN_SECRET", default="")

# ---------------------------------------------------------------------------
# Authentication redirects
# ---------------------------------------------------------------------------
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
