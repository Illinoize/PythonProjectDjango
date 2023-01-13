"""Importing models"""
from django.db import models  # pylint: disable=E0401
from django.utils.crypto import get_random_string  # pylint: disable=E0401


class Wallet(models.Model):  # pylint: disable=R0903
    """Creating Wallet model"""
    RANDOM_NAME = get_random_string(length=8)  # Name must consists of 8 symbols
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
    # Name must consists of 8 symbols
    type = models.CharField(choices=CARD_CHOICE, max_length=100, default='Visa')
    currency = models.CharField(choices=CURRENCY_CHOICE, max_length=100, default='USD')

    start_balance = 0.00  # to get float number
    if currency in ('USD', 'EUR'):
        start_balance = (start_balance + 3) * 100 / 100  # start balance for EUR and USD = 3.00
    else:
        start_balance = (start_balance + 100) * 100 / 100  # start balance for RUB = 100.00

    balance = models.FloatField(max_length=100, blank=False, default=start_balance)
    created_on = models.DateTimeField(auto_now=True)
    modified_on = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='wallets', on_delete=models.CASCADE)
