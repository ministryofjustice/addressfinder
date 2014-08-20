"""
WSGI config for addressfinder project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os
from os.path import abspath, dirname
from sys import path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "addressfinder.settings")

SITE_ROOT = dirname(dirname(abspath(__file__)))
path.append(SITE_ROOT)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
