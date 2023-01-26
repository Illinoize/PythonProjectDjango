"""Importing AppConfig"""
from django.apps import AppConfig  # pylint: disable=E0401


class WalletsConfig(AppConfig):  # pylint: disable=R0903
    """Wallets Config"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wallets'
