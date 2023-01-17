"""Importing models"""
from django.db import models  # pylint: disable=E0401


class Wallet(models.Model):  # pylint: disable=R0903
    """Creating Wallet model"""
    CARD_CHOICE = (
        ('Visa', 'Visa'),
        ('Mastercard', 'Mastercard'),
    )
    CURRENCY_CHOICE = (
        ('USD', 'USD'),
        ('RUB', 'RUB'),
        ('EUR', 'EUR'),
    )

    name = models.CharField(max_length=8, blank=False, default='')
    # Name must consists of 8 symbols
    type = models.CharField(choices=CARD_CHOICE, max_length=100, default='Visa')
    currency = models.CharField(choices=CURRENCY_CHOICE, max_length=100, default='USD')
    balance = models.FloatField(default=0)
    created_on = models.DateTimeField(auto_now=True)
    modified_on = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='wallets',
                              on_delete=models.CASCADE, blank=False)


# class Transaction(models.Model):  # pylint: disable=R0903
#     """Creating Transaction model"""
#     STATUS_CHOICES = (
#         ('PAID', 'PAID'),
#         ('FAILED', 'FAILED'),
#     )
#
#     sender = models.ForeignKey(Wallet,
#     related_name='name', on_delete=models.CASCADE, blank=False),
#     receiver = models.ForeignKey(Wallet,
#     related_name='name', on_delete=models.CASCADE, blank=False),
#     transfer_amount = models.DecimalField(default=0)
#     commission = models.FloatField(default=0)
#     status = models.CharField(choices=STATUS_CHOICES, default='PAID')
#     timestamp = models.DateTimeField(auto_now_add=True)
