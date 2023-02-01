# pylint: disable=import-error  disable=line-too-long  disable=consider-using-f-string
"""Importing models"""
import datetime

from django.db import models, transaction
from django.utils.crypto import get_random_string


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
    type = models.CharField(choices=CARD_CHOICE, max_length=100, default='Visa')
    currency = models.CharField(choices=CURRENCY_CHOICE, max_length=100, default='USD')
    balance = models.FloatField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='wallets',
                              on_delete=models.CASCADE, blank=False)

    def save(self, *args, **kwargs):
        """Creating wallet"""
        if Wallet.objects.filter(owner=self.owner).count() > 4:
            raise Exception('You have maximum wallets')
        self.name = get_random_string(length=8).upper()  # Name must consists of 8 symbols
        if self.currency == 'RUB':
            self.balance = 100  # 100.00 start balance for currency RUB
            self.balance = float('{:.2f}'.format(self.balance))  # Balance should be rounded up to 2 decimals
        else:
            self.balance = 3  # 3.00 start balance for currency USD, EUR
            self.balance = float('{:.2f}'.format(self.balance))  # Balance should be rounded up to 2 decimals
        self.created_on = datetime.datetime.now()
        self.modified_on = datetime.datetime.now()
        super().save(*args, **kwargs)

    def update(self, balance):
        """Updating wallet"""
        self.balance = balance
        self.balance = float('{:.2f}'.format(self.balance))  # Balance should be rounded up to 2 decimals
        self.modified_on = datetime.datetime.now()
        super().save()


class Transaction(models.Model):  # pylint: disable=R0903
    """Creating Transaction model"""
    STATUS_CHOICES = (
        ('PAID', 'PAID'),
        ('FAILED', 'FAILED'),
    )

    sender = models.ForeignKey(Wallet,
                               related_name='sender', on_delete=models.CASCADE, blank=False)
    receiver = models.ForeignKey(Wallet,
                                 related_name='receiver', on_delete=models.CASCADE, blank=False)
    transfer_amount = models.FloatField(default=0)
    commission = models.FloatField(default=0)
    status = models.CharField(choices=STATUS_CHOICES, default='PAID', max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def make_transaction(self):
        """Preparing info for transaction and checking users"""
        sender = self.sender
        receiver = self.receiver
        amount = self.transfer_amount
        if sender.owner == receiver.owner:
            self.check_currency(sender, receiver, amount)
        else:
            self.commission = self.transfer_amount * 0.10  # If you send money to another user, you pay fixed commission
            self.transfer_amount -= self.commission
            amount = self.transfer_amount
            self.check_currency(sender, receiver, amount)

    def check_currency(self, sender, receiver, amount):
        """Checking whether wallets have the same currency"""
        if sender.currency == receiver.currency:
            self.check_balance(sender, receiver, amount)
        else:
            self.status = 'FAILED'
            raise Exception('You cannot transfer amount between wallets with different currencies')

    def check_balance(self, sender, receiver, amount):
        """Checking balance and provide required action"""
        if sender.balance >= amount:
            with transaction.atomic():
                sender.balance -= amount
                sender.update(balance=sender.balance)
                receiver.balance += amount
                receiver.update(balance=receiver.balance)
                self.status = 'PAID'
        else:
            self.status = 'FAILED'
            raise Exception('You do not have enough money')

    def save(self, *args, **kwargs):
        """Creating transaction"""
        self.make_transaction()
        self.timestamp = datetime.datetime.now()
        super().save(*args, **kwargs)
