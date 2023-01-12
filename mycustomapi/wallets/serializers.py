"""Importing model and serializers"""
from rest_framework import serializers  # pylint: disable=E0401
from wallets.models import Wallet  # pylint: disable=E0401


class WalletSerializer(serializers.ModelSerializer):  # pylint: disable=R0903
    """Create serialization for Wallet model"""
    class Meta:  # pylint: disable=R0903
        """Create Meta class for model"""
        model = Wallet
        fields = ('id',
                  'name',
                  'type',
                  'currency',
                  'balance',
                  'created_on',
                  'modified_on',)
