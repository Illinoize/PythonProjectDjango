# pylint: disable=import-error  disable=redefined-outer-name
"""Importing modules to prepare data for tests"""
import pytest

from django.contrib.auth.models import User



@pytest.fixture(scope='function')
def create_user():
    """Creating an user instance"""
    user1 = User.objects.create(
        username='user1',
        password='userpassword'
    )
    user2 = User.objects.create(
        username='user2',
        password='new_password'
    )
    return user1, user2


# @pytest.fixture(scope='function')
# def sending_wallet(create_user):
#     """Creating a wallet instance as a sender"""
#     wallet1 = Wallet.objects.create(
#         name='TESTNAME',
#         type='Visa',
#         currency='RUB',
#         balance='100',
#         created_on='12.12.2012',
#         modified_on='13.12.2013',
#         owner=create_user
#     )
#     return wallet1
#
#
# @pytest.fixture(scope='function')
# def receiving_wallet(create_user):
#     """Creating a wallet instance as a receiver"""
#     wallet2 = Wallet.objects.create(
#         name='NAMETEST',
#         type='Mastercard',
#         currency='RUB',
#         balance='100',
#         created_on='15.12.2012',
#         modified_on='16.12.2013',
#         owner=create_user
#     )
#     return wallet2
#
#
# @pytest.fixture(scope='function')
# def make_transaction(sending_wallet, receiving_wallet):
#     """Creating a transaction instance"""
#     transaction1 = Transaction.objects.create(
#         sender=sending_wallet,
#         receiver=receiving_wallet,
#         transfer_amount=23,
#         commission=0,
#         status='PAID',
#         timestamp='25.01.2023'
#     )
#     return transaction1
