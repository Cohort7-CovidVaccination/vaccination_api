"""
WSGI config for vaccination project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from vaccination_app.fill_data import Fill_countries

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaccination.settings')

application = get_wsgi_application()
Fill_countries()