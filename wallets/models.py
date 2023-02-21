# pylint: disable=import-error  disable=line-too-long  disable=consider-using-f-string
"""Importing models"""


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
    modified_on = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', related_name='wallets',
                              on_delete=models.CASCADE, blank=False)

    def save(self, *args, **kwargs):
        """Creating wallet"""
        if Wallet.objects.filter(owner=self.owner).count() > 4:
            raise ValueError('You have maximum wallets')
        self.name = get_random_string(length=8).upper()  # Name must consists of 8 symbols
        if self.currency == 'RUB':
            self.balance = round(100, 2)  # 100.00 start balance for currency RUB
            # Balance should be rounded up to 2 decimals
        else:
            self.balance = round(3, 2)  # 3.00 start balance for currency USD, EUR
            # Balance should be rounded up to 2 decimals
        super().save(*args, **kwargs)

    def update(self, balance: int):
        """Updating wallet"""
        self.balance = round(balance, 2)  # Balance should be rounded up to 2 decimals
        super().save()

    def __str__(self):
        return "%s: %s, %s" % (self.owner, self.name, self.currency)


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
    commission = models.FloatField(default=0)  # default commission for one user is 0
    status = models.CharField(choices=STATUS_CHOICES, default='PAID', max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def make_transaction(self):
        """Preparing info for transaction and checking users"""
        sender = self.sender
        receiver = self.receiver
        if sender.owner == receiver.owner:
            self.check_currency(sender, receiver)
        else:
            self.change_commission()
            self.check_currency(sender, receiver)

    def change_commission(self):
        """Changing commission for transactions between different users"""
        self.commission = round(self.transfer_amount * 0.10, 2)
        # If you send money to another user, you pay fixed commission

    def check_currency(self, sender: Wallet, receiver: Wallet):
        """Checking whether wallets have the same currency"""
        if sender.currency == receiver.currency:
            self.check_balance(sender, receiver)
        else:
            self.status = 'FAILED'
            raise ValueError('You cannot transfer amount between wallets with different currencies')

    def check_balance(self, sender: Wallet, receiver: Wallet):
        """Checking balance and provide required action"""
        if sender.balance >= self.transfer_amount + self.commission:
            with transaction.atomic():
                sender.balance -= (self.transfer_amount + self.commission)
                sender.update(balance=sender.balance)
                receiver.balance += self.transfer_amount
                receiver.update(balance=receiver.balance)
                self.status = 'PAID'
        else:
            self.status = 'FAILED'
            raise ValueError('You do not have enough amount for transaction')

    def save(self, *args, **kwargs):
        """Creating transaction"""
        self.make_transaction()
        super().save(*args, **kwargs)
