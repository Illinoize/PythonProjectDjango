# pylint: disable=import-error  disable=unused-argument  disable=too-few-public-methods
"""Importing test module"""
import pytest

from rest_framework.test import APIClient

from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db
client = APIClient()


@pytest.mark.django_db
class TestUsers:
    """Creating test class for user model"""
    def test_my_user(self, create_user):
        """Creating test function for user model"""
        user = User.objects.get(username='user1')
        assert user.username == 'user1'
        assert user.id == 1
        assert user.password is not None


@pytest.mark.django_db
class TestWallet:
    """Creating test class for Wallet"""
    def test_new_wallet(self, create_user):
        """Testing creating new wallet"""
        # Only authenticated users can create wallets
        user = User.objects.get(username="user1")
        client.force_authenticate(user=user)

        response = client.post("/wallets/")

        assert response.status_code == 201

        data = response.data

        assert data["balance"] != 0
        assert len(data["name"]) == 8
        assert data["currency"] == "USD"

        new_response = client.get("/wallets/")
        assert new_response.status_code == 200


@pytest.mark.django_db(transaction=True)
class TestTransaction:
    """Creating test class for Transaction"""
    def test_new_transaction(self, create_user):
        """Testing transaction"""
        # Creating a wallet for user1 and logout
        user = User.objects.get(username="user1")
        client.force_authenticate(user=user)
        wallet1 = client.post("/wallets/")
        client.logout()

        # Creating a wallet for user2
        user2 = User.objects.get(username="user2")
        client.force_authenticate(user=user2)
        wallet2 = client.post("/wallets/", dict(type="Mastercard", currency="USD"))

        # Checking whether both wallets were created
        assert wallet1.status_code == 201
        assert wallet2.status_code == 201

        # Creating a transaction
        transaction = client.post("/transactions/", dict(sender=wallet2.data["name"],
                                                         receiver=wallet1.data["name"],
                                                         transfer_amount=1))

        data = transaction.data

        assert transaction.status_code == 201
        assert data["status"] == "PAID"
        assert data["transfer_amount"] == 1
        assert data["commission"] != 0
