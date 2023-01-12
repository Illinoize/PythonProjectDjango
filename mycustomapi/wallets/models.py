"""Importing models"""
from django.db import models  # pylint: disable=E0401
from django.utils.crypto import get_random_string  # pylint: disable=E0401

RANDOM_NAME = get_random_string(length=8)
CARD_CHOICE = (
    (1, 'Visa'),
    (2, 'Mastercard'),
)
CURRENCY_CHOICE = (
    (1, 'USD'),
    (2, 'RUB'),
    (3, 'EUR'),
)


class Wallet(models.Model):  # pylint: disable=R0903
    """Creating Wallet model"""
    name = models.CharField(max_length=8, blank=False, default=RANDOM_NAME.upper())
    type = models.CharField(choices=CARD_CHOICE, max_length=100, default=1)
    currency = models.CharField(choices=CURRENCY_CHOICE, max_length=100, default=1)
    balance = models.FloatField(max_length=100, blank=False, default='')
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now_add=True)
