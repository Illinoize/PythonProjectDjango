"""Importing models"""
from django.db import models  # pylint: disable=E0401
from django.utils.crypto import get_random_string  # pylint: disable=E0401


class Wallet(models.Model):  # pylint: disable=R0903
    """Creating Wallet model"""
    RANDOM_NAME = get_random_string(length=8)
    CARD_CHOICE = (
        ('Visa', 'Visa'),
        ('Mastercard', 'Mastercard'),
    )
    CURRENCY_CHOICE = (
        ('USD', 'USD'),
        ('RUB', 'RUB'),
        ('EUR', 'EUR'),
    )

    name = models.CharField(max_length=8, blank=False, default=RANDOM_NAME.upper())
    type = models.CharField(choices=CARD_CHOICE, max_length=100, default='Visa')
    currency = models.CharField(choices=CURRENCY_CHOICE, max_length=100, default='USD')
    balance = models.FloatField(max_length=100, blank=False, default=0.00)
    created_on = models.DateTimeField(auto_now=True)
    modified_on = models.DateTimeField(auto_now_add=True)
