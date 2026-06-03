"""
ASGI config for the news_project.

This module exposes the ASGI callable as a module-level variable named
``application``. It allows Django to serve asynchronous requests and is used
by ASGI servers such as Daphne or Uvicorn.

For more information, see:
https://docs.djangoproject.com/en/stable/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set the default Django settings module for the ASGI application.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_project.settings")

# Create the ASGI application callable that servers will use.
application = get_asgi_application()
