"""
WSGI config for mycustomapi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application  # pylint: disable=E0401

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycustomapi.settings')  # pylint: disable=E1101

application = get_wsgi_application()
