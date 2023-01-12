"""Importing models"""
from django.db import models  # pylint: disable=E0401
from django.utils.crypto import get_random_string  # pylint: disable=E0401


class Wallet(models.Model):  # pylint: disable=R0903
    """Creating Wallet model"""
    RANDOM_NAME = get_random_string(length=8)
    CARD_CHOICE = (
        ('V', 'Visa'),
        ('M', 'Mastercard'),
    )
    CURRENCY_CHOICE = (
        ('U', 'USD'),
        ('R', 'RUB'),
        ('E', 'EUR'),
    )

    name = models.CharField(max_length=8, blank=False, default=RANDOM_NAME.upper())
    type = models.CharField(choices=CARD_CHOICE, max_length=100, default='V')
    currency = models.CharField(choices=CURRENCY_CHOICE, max_length=100, default='U')
    balance = models.FloatField(max_length=100, blank=False, default=0.0)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now_add=True)
