import os
import sys
import django

# --- Django setup ------------------------------------------------------------
sys.path.insert(0, os.path.abspath('../..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'news_project.settings'
django.setup()

# --- Project information -----------------------------------------------------
project = 'Django News'
author = 'Khumo'
release = '1.0'

# --- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

autodoc_mock_imports = [
    "django",
    "rest_framework",
    "newsapp.models",
    "newsapp.serializers",
    "newsapp.permissions",
    "newsapp.signals",
    "newsapp.views",
]

templates_path = ['_templates']
exclude_patterns = ["**/tests.py", "**/tests/*"]



# --- HTML output -------------------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']
