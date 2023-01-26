# pylint: disable=import-error
"""Importing models"""
from django.db import models
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
    created_on = models.DateTimeField(auto_now=True)
    modified_on = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='wallets',
                              on_delete=models.CASCADE, blank=False)

    def save(self, *args, **kwargs):
        """Creating wallet"""
        if Wallet.objects.count() > 4:
            raise Exception('You have maximum wallets')
        self.name = get_random_string(length=8).upper()  # Name must consists of 8 symbols
        if self.currency == 'RUB':
            self.balance = format(100, '2f')  # 100.00 start balance for currency RUB
        else:
            self.balance = format(3, '2f')  # 3.00 start balance for currency USD, EUR
        super().save(*args, **kwargs)


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

    def check_balance(self, input_1, input_2):
        """Checking balance and provide required action"""
        if input_1.filter(id=self.pk) >= input_2.filter(id=self.pk):
            input_1.balance.entry_set.remove(self.transfer_amount)
            input_2.balance.entry_set.add(self.transfer_amount)
            self.status = 'PAID'
        else:
            self.status = 'FAILED'

    def check_currency(self, input_1, input_2):
        """Checking whether wallets have the same currency"""
        if input_1.filter(id=self.pk) == input_2.filter(id=self.pk):
            self.check_balance(input_1, input_2)
        else:
            self.status = 'FAILED'

    def save(self, *args, **kwargs):
        """Creating transaction"""
        sender = Transaction.objects.select_related('sender')
        receiver = Transaction.objects.select_related('receiver')
        if sender.filter(sender=self.pk) == receiver.filter(receiver=self.pk):
            self.check_currency(sender, receiver)
        else:
            self.commission = 0.10  # commission for transaction between different owners
            self.transfer_amount *= self.commission
            self.check_currency(sender, receiver)
        super().save(*args, **kwargs)
