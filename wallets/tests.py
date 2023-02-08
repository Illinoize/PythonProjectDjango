# pylint: disable=import-error  disable=unused-argument  disable=too-few-public-methods
"""Importing test module"""
import pytest

from django.contrib.auth.models import User


pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestUsers:
    """Creating test class for user model"""
    def test_my_user(self, create_user):
        """Creating test function for user model"""
        new_user = User.objects.get(username='user1')
        assert new_user.username == 'user1'
        assert new_user.id == 1
        assert new_user.password is not None


@pytest.mark.django_db
class TestWallets:
    """Creating test class for wallet model"""
    def test_new_wallets(self, sending_wallet, create_user):
        """Creating test function for wallet model"""
        assert sending_wallet is not None
        assert sending_wallet.balance == 100
        assert sending_wallet.type == 'Visa'

    def test_another_wallet(self, receiving_wallet, create_user):
        """Creating test function for another wallet model"""
        assert receiving_wallet.currency == 'RUB'
        assert receiving_wallet.owner == create_user


@pytest.mark.django_db(transaction=True)
class TestTransactions:
    """Creating test class for Transaction model"""
    def test_my_transaction(self, sending_wallet, receiving_wallet, make_transaction):
        """Creating test function for transaction model"""
        assert sending_wallet.balance - make_transaction.transfer_amount >= 0
        assert sending_wallet.currency == receiving_wallet.currency
        assert sending_wallet.owner == receiving_wallet.owner
        assert make_transaction.commission != 0.10
