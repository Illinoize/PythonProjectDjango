"""
ASGI config for testetst project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application  # pylint: disable=E0401

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycustomapi.settings')  # pylint: disable=E1101

application = get_asgi_application()
