"""
WSGI config for the news_project.

This module exposes the WSGI callable used by Django’s deployment servers
such as Gunicorn or uWSGI. It sets the default settings module and creates
the WSGI application object that servers use to forward HTTP requests into
the Django application.

For more information, see:
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")
application = get_wsgi_application()
