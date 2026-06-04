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

templates_path = ['_templates']
exclude_patterns = []

# --- HTML output -------------------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']
